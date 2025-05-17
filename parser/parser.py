import asyncio
import re
from functools import wraps
from typing import Any, Self

import httpx
from httpx import URL, Response
from bs4 import BeautifulSoup

from .dto import ItemCard
from .js import calc_card_url


def ensure_success(request_func):
    @wraps(request_func)
    async def wrapper(*args, **kwargs):
        r: httpx.Response = await request_func(*args, **kwargs)
        if r.status_code != 200:
            RuntimeError(
                f"Request function {request_func.__name__} failed.\n"
                f"args: {args};\n"
                f"kwargs: {kwargs};\n"
                f"r.text: {r.text[:200]}"
            )
        return r
    
    return wrapper


class WBParser:
    def __init__(self, urls_to_parse: list[URL]):
        self.client: httpx.AsyncClient = None
        self.headers: dict[str, str] | None = None
        self.proxies: dict[str, str] | None = None

        self.item_urls: list[URL] = urls_to_parse
        self.item_cards: list[ItemCard] = []
    
    async def __aenter__(self) -> Self:
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()
    
    async def run(self):
        tasks = [self.parse_item(url) for url in self.item_urls]
        await asyncio.gather(*tasks)
    
    async def parse_item(self, item_url: URL):
        print(f'Parsing {item_url}')
        r = await self.get_item_page(item_url)
        item_page_html = r.text
        
        index_js_url = self.parse_index_script_url(item_page_html)
        r = await self.get_js_script(index_js_url)
        index_js_script = r.text
        card_url_funcs = self.parse_index_funcs(index_js_script)
        
        item_nm_id = item_url.path.split('/')[-2]
        card_url = calc_card_url(item_nm_id, card_url_funcs)
        r = await self.get_item_card(card_url)
        card_info = r.json()
        item_card = self.parse_card_info(card_info)
        self.item_cards.append(item_card)
        print(f'Finished {item_url}')
        
    @ensure_success
    async def get_item_page(self, item_url: URL) -> Response:
        r = await self.client.get(item_url)

        return r

    @ensure_success
    async def get_js_script(self, script_url: URL) -> Response:
        r = await self.client.get(script_url)

        return r
    
    @ensure_success
    async def get_item_card(self, card_url: URL) -> Response:
        r = await self.client.get(card_url)

        return r
    
    def parse_index_script_url(self, html: str) -> URL:
        pattern = re.compile(r"/index[^\"']*\.js$")
        
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find("script", src=pattern)

        return f'https:{script["src"]}'
    
    def parse_index_funcs(self, js_txt: str) -> tuple[str]:
        basket_pattern = r"volHostV2\s*:\s*\(.*?\)\s*=>\s*\{.*?\},"
        match = re.search(basket_pattern, js_txt)

        if match:
            basket_id_func = match.group(0)[:-1]
        
        card_pattern = r"constructHostV2\s*:\s*\(.*?\)\s*=>\s*\{.*?\}}"
        match = re.search(card_pattern, js_txt)

        if match:
            card_url_func = match.group(0)[:-2] + ';}'

        fix_js_pattern = re.compile(r";return.*?;", re.DOTALL | re.VERBOSE)
        replacement = ';i = u.volHostV2(n, r); return `https://${i}/part${s}/${n}`;'
        card_url_func = fix_js_pattern.sub(replacement, card_url_func)
        
        return (basket_id_func, card_url_func)
    
    def parse_card_info(self, card_info: Any) -> None:
        item_card = ItemCard(**card_info)
        return item_card

