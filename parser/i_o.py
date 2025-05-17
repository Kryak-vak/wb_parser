import json
from pathlib import Path

from httpx import URL

from .dto import ItemCard


def read_urls():
    path = Path(__file__).parent.parent / 'data' / 'urls.json'
    with open(path, 'r', encoding='utf-8') as f:
        urls: list[URL] = [URL(url) for url in json.load(f)]

        return urls


def write_items(items: list[ItemCard]) -> None:
    path = Path(__file__).parent.parent / 'data' / 'output.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(
            [item.model_dump(mode='json') for item in items],
            f,
            ensure_ascii=False,
            indent=4
        )
