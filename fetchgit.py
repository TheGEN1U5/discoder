from gitingest import ingest_async
import asyncio

async def fetch_directory_tree(github_link):
    output = await ingest_async(github_link)
    tree = output[1]
    return tree


async def fetch_files(github_link, names):
    content = ""
    content = await ingest_async(github_link, 50*1024*1024, names)[2]
    return content

# print(fetch_files("https://github.com/SaiyamLohia/Cloud_Gardening", ["*/RainCloud.cs", "*/Flower.cs"]))
# print(fetch_files("https://github.com/SaiyamLohia/Cloud_Gardening", "*/Flower.cs"))

