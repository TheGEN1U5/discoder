from mira_sdk import MiraClient, Flow, File
from dotenv import load_dotenv
import os

load_dotenv()
client = MiraClient(config={"API_KEY": os.getenv("MIRA_API_KEY")})

def discussion_summariser(discussion=''):
    summarizer_flow = Flow(source="flows/summarizer-flow.yaml")
    input_dict = {"discussion" : discussion}
    response = client.flow.test(summarizer_flow, input_dict)

    return response['result']

async def readme_summariser(readme):
    return readme