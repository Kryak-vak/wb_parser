import asyncio

from parser.parser import WBParser
from parser.i_o import read_urls


async def main():
    urls_to_parse = read_urls()

    async with WBParser(urls_to_parse) as parser:
        await parser.run()


if __name__ == "__main__":
    asyncio.run(main())
