import asyncio

from parser.parser import WBParser
from parser.i_o import read_urls, write_items


async def main():
    urls_to_parse = read_urls()
    
    print(f'Parsing started')
    async with WBParser(urls_to_parse) as parser:
        await parser.run()
        write_items(parser.item_cards)
    print(f'Parsing finished')


if __name__ == "__main__":
    asyncio.run(main())
