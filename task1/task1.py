import argparse
import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile
from collections import defaultdict
import logging

parser = argparse.ArgumentParser(
    prog="File sorter",
    description="File sorter by extension",
    epilog="params -s source -t target",
)

parser.add_argument("-s", "--source", required=True, help="Source dir")
parser.add_argument("-t", "--target", required=True, help="Target dir")

args = parser.parse_args()

print(args.source, args.target)

source = AsyncPath(args.source)
target = AsyncPath(args.target)


async def main():
    logging.debug("main started")
    logging.debug(f"{source = }")
    if await source.exists():
        await read_folder(source)


async def read_folder(src):
    logging.debug("read_folder started")
    logging.debug(f"{src = }")
    if await src.exists():
        async for file in src.iterdir():
            if await file.is_dir():
                await read_folder(file)
            else:
                await copy_file(file)


async def copy_file(file):
    logging.debug("copy_file started")
    logging.debug(f"{file = }")
    folder = target / file.suffix[1:]
    try:
        await folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, folder / file.name)
        logging.debug(f"{file = } completed")
    except OSError as e:
        logging.error(e)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    asyncio.run(read_folder(source))
