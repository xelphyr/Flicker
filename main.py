from slack_bot_web_hook import slack_bot
import slack
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

