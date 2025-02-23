from mira_sdk import MiraClient, Flow, File
from token_checker import token_checker

tokens = token_checker()
if not tokens[0]:
	print("Please enter your MIRA API Key manually in your .env file.")
	__import__('sys').exit(0)
mira_token = tokens[2]
client = MiraClient(config={"API_KEY": mira_token})

def discussion_summariser(discussion:str='', readme_summary:str='', tech_stack:str=''):
    summariser = Flow(source="flows/discussion-summariser-flow.yaml")
    input_dict = {"discussion": discussion, "readme_summary" : readme_summary, "tech_stack": tech_stack}
    response = client.flow.test(summariser, input_dict)
    output = response["result"].split("```")
    op_dict = output[1].replace("json", "")
    op_summary = output[2]
    
    if(op_summary.strip().startswith('Summary: ')):
        op_summary = op_summary.split('Summary: ')[1]
    elif(op_summary.strip().startswith('**Summary:** ')):
        op_summary = op_summary.split('**Summary:** ')[1]
    elif(op_summary.strip().startswith('**Summary**: ')):
        op_summary = op_summary.split('**Summary**: ')[1]
    elif(op_summary.strip().startswith('Summary: \n')):
        op_summary = op_summary.split('Summary: \n')[1]
    elif(op_summary.strip().startswith('**Summary:** \n')):
        op_summary = op_summary.split('**Summary:** \n')[1]
    elif(op_summary.strip().startswith('**Summary**: \n')):
        op_summary = op_summary.split('**Summary**: \n')[1]
    elif(op_summary.strip().startswith('Summary:\n')):
        op_summary = op_summary.split('Summary:\n')[1]
    elif(op_summary.strip().startswith('**Summary:**\n')):
        op_summary = op_summary.split('**Summary:**\n')[1]
    elif(op_summary.strip().startswith('**Summary**:\n')):
        op_summary = op_summary.split('**Summary**:\n')[1]
    
    op_summary = op_summary.lstrip()
    return tuple([op_dict, op_summary])

def readme_summariser(readme:str=''):
    summariser = Flow(source="flows/readme-summariser-flow.yaml")
    input_dict = {"readme": readme}
    response = client.flow.test(summariser, input_dict)
    return response['result']

def files_summariser(tree:str='', json_features:str='', readme_summary:str='', tech_stack:str=''):
    summariser = Flow(source="flows/files-summariser-flow.yaml")
    input_dict = {"tree" : tree, "json_features": json_features, "readme_summary":  readme_summary, "tech_stack": tech_stack}
    response = client.flow.test(summariser, input_dict)
    output_list = response['result'].replace('`', '').split(', ')
    # output_list = list(output_string)
    return output_list

def codeblock_creator(tree:str='', file_paths:list=[], file_contents:str='', json_features:str='', tech_stack:str='', readme_summary:str=''):
    summariser = Flow(source="flows/codeblock-creator-flow.yaml")
    input_dict = {"tree" : tree, "file_paths": str(file_paths), "file_contents": file_contents, "json_features": json_features, "tech_stack": tech_stack, "readme_summary": readme_summary}
    response = client.flow.test(summariser, input_dict)
    return response['result'].replace("##", "#")