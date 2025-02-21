from mira_sdk import MiraClient, Flow, File
from dotenv import load_dotenv
import os

load_dotenv()
client = MiraClient(config={"API_KEY": os.getenv("MIRA_API_KEY")})

def discussion_summariser(discussion=""):
    summariser = Flow(source="flows/discussion-summariser-flow.yaml")
    input_dict = {"discussion": discussion}
    response = client.flow.test(summariser, input_dict)
    output = response["result"].split("```")
    op_dict = output[1].replace("json", "")
    op_summary = output[2]
    return tuple([op_dict, op_summary])


async def readme_summariser(readme=''):
    return readme
