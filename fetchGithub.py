from gitingest import ingest


def fetch_directory_tree(github_link):
    tree = ingest(github_link)[1]
    return tree


def fetch_files(github_link, names):
    content = ""
    if type(names) == type(""):
        content += ingest(github_link, 50*1024, names)[2]
        return content

    for name in names:
        content += ingest(github_link, 50*1024, name)[2]

    return content

# print(fetch_files("https://github.com/SaiyamLohia/Cloud_Gardening", ["*/RainCloud.cs", "*/Flower.cs"]))
# print(fetch_files("https://github.com/SaiyamLohia/Cloud_Gardening", "*/Flower.cs"))

