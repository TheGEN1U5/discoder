from gitingest import ingest_async
import asyncio

async def fetch_directory_tree(github_link):
    output = await ingest_async(github_link)
    tree = output[1]
    return tree


async def fetch_files(github_link, names):
    content = ""
    if isinstance(names, str):
        # Use existing event loop instead of asyncio.run()
        result = await ingest_async(github_link, 50*1024, names)
        content += result[2]
    else:
        for name in names:
            result = await ingest_async(github_link, 50*1024, name)
            content += result[2]
    return content


