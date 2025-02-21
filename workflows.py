from mira_sdk import MiraClient, Flow, File
from token_checker import token_checker

tokens = token_checker()
if not tokens[0]:
	print("Please enter your MIRA API Key manually in your .env file.")
	__import__('sys').exit(0)
mira_token = tokens[2]
client = MiraClient(config={"API_KEY": mira_token})

def discussion_summariser(discussion:str=''):
    summariser = Flow(source="flows/discussion-summariser-flow.yaml")
    input_dict = {"discussion": discussion}
    response = client.flow.test(summariser, input_dict)
    output = response["result"].split("```")
    op_dict = output[1].replace("json", "")
    op_summary = output[2]
    return tuple([op_dict, op_summary])

async def readme_summariser(readme:str=''):
    summariser = Flow(source="flows/readme-summariser-flow.yaml")
    input_dict = {"readme": readme}
    response = client.flow.test(summariser, input_dict)
    return response['result']

def files_summariser(tree:str='', json_features:str=''):
    summariser = Flow(source="flows/files-summariser-flow.yaml")
    input_dict = {"tree" : tree, "json_features": json_features}
    response = client.flow.test(summariser, input_dict)
    return response['result']
