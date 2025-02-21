import os
from dotenv import load_dotenv

def token_checker():
    return_tuple = [0, '', '']
    if os.path.exists(r'.env'):
        load_dotenv()
        discord_token = ''
        mira_api = ''
        try:
            discord_token = os.getenv('DISCORD_TOKEN')
            mira_api = os.getenv('MIRA_API_KEY')
        except:
            return tuple(return_tuple)
        else:
            return_tuple[0] = 1
            return_tuple[1] = discord_token
            return_tuple[2] = mira_api
            return tuple(return_tuple)


    else:
	    with open('.env', 'x+') as f:
		    dc_token = input("Enter your token for the discord bot: ")
		    mira_token = input("Enter your token for MIRA API: ")
		    dc_token_str = f"DISCORD_TOKEN={dc_token}\n"
		    mira_token_str = f"MIRA_API_KEY={mira_token}\n"
		    f.write(dc_token_str)
		    f.write(mira_token_str)
		    return (1, dc_token, mira_token)


