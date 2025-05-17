import json
from httpx import URL
from pathlib import Path


def read_urls():
    path = Path(__file__).parent.parent / 'data' / 'urls.json'
    with open(path, 'r', encoding='utf-8') as file:
        urls: list[URL] = [URL(url) for url in json.load(file)]

        return urls
