
# Discoder
Discoder is an open-source Discord bot that integrates Git, GitHub and MIRA's power all in one teeny-tiny bot that rules them all! This bot was made as a part of a hackathon named Ctrl+Shift+Intelligence hosted by the Club Of ProgrammerS (COPS) at Indian Institute of Technology (B. H. U.) Varanasi as a part of COPS' Week '25. 

## Installation

1. Clone the repository:
```
git clone https://github.com/your-username/discord-project-manager-bot.git
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory and add your Discord bot token and MIRA API key:
```
DISCORD_TOKEN=your_discord_bot_token
MIRA_API_KEY=your_mira_api_key
```

4. Run the bot:
```
python main.py
```

## Usage

The bot has the following commands:

1. `?createproject <project_name>`: Creates a new project channel and initializes the project.
2. `?deleteproject`: Deletes the current project channel and all associated files.
3. `?startdiscussion <discussion_name>`: Starts a new discussion thread for the current project.
4. `?enddiscussion`: Ends the current discussion thread and saves the conversation summary.

## API

The bot uses the following APIs:

1. Discord API: For interacting with the Discord server and managing channels, threads, and messages.
2. MIRA API: For summarizing README files and discussion threads.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Submit a pull request.

## Authors

  

- Tanishq Ahuja [@TheGEN1U5](https://www.github.com/TheGEN1U5)
- Saiyam Lohia [@SaiyamLohia](https://www.github.com/SaiyamLohia)
- Pranav Arora [@arora-pranav](https://www.github.com/arora-pranav)
- Saikat Ghorai [@ghoraisaikat](https://www.github.com/ghoraisaikat)


