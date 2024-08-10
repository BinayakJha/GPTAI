import os
import click
from dotenv import load_dotenv
from colorama import Fore, Style

# Load environment variables from .env file
load_dotenv()

CONFIG_PATH = os.path.expanduser('~/.git_ai_config')

class ConfigManager:


    def save_token(self, token):
        with open(CONFIG_PATH, 'w') as config_file:
            config_file.write(token)

    def load_token(self):
        # First try to load from the .env file
        token = os.getenv('GITHUB_TOKEN')
        if token:
            return token

        # If not found, fall back to config file
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as config_file:
                return config_file.read().strip()
        return None

    def prompt_for_token(self):
        return click.prompt(f'{Fore.BLUE}Enter your GitHub token:{Style.RESET_ALL}', hide_input=True)
