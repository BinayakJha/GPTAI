import os
import json
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from colorama import Fore, Style
# Load environment variables
load_dotenv()

class CodeChecker:
    def __init__(self, repo_path):

    def check_code(self):
        print(f'Checking code quality and security for repository at {self.repo_path}...')
        with open('main.py', 'r') as file:
            code_content = file.read()

        prompt = f"Analyze the following file for quality, security, and potential issues in the file, Divide the analysis in specific parts with the titles like quality, bugs, etc. Also give some ways to fix the code by giving the code and give the correct line number for them. Don't give any big explanations, be to the point. \n\n{code_content}"

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                },
                data=json.dumps({
                    "model": "meta-llama/llama-3.1-8b-instruct:free",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                })
            )

            if response.status_code == 200:
                response_json = response.json()
                analysis_text = response_json['choices'][0]['message']['content']

                print(f'{Fore.BLUE}Code analysis completed:{Style.RESET_ALL}')
                print(f'{Fore.CYAN}{Style.BRIGHT}{analysis_text}{Style.RESET_ALL}')

                user_query = input('Do you want to continue with the AI to get more information and also fix the code? (yes/no): ')
                if user_query.lower() == 'yes':
                    while True:
                        user_query = input('Enter your query: ')
                        if user_query.lower() == 'exit':
                            break

                        follow_up_response = requests.post(
                            url="https://openrouter.ai/api/v1/chat/completions",
                            headers={
                                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                            },
                            data=json.dumps({
                                "model": "meta-llama/llama-3.1-8b-instruct:free",
                                "messages": [
                                    {"role": "system", "content": analysis_text},
                                    {"role": "user", "content": user_query}
                                ]
                            })
                        )

                        follow_up_text = follow_up_response.json()['choices'][0]['message']['content']
                        print(f'{Fore.CYAN}{Style.BRIGHT}{follow_up_text}{Style.RESET_ALL}')
                else:
                    print('Exiting the code analysis...')
            else:
                genai.configure(api_key=self.gemini_api_key)
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro"
                )
                response = model.generate_content(prompt)
                print(f'{Fore.BLUE}Code analysis completed:{Style.RESET_ALL}')
                print(f'{Fore.CYAN}{Style.BRIGHT}{response.text}{Style.RESET_ALL}')

                user_query = input(f'{Fore.BLUE}Do you want to continue with the AI to get more information and also fix the code? (yes/no): {Style.RESET_ALL}')
                if user_query.lower() == 'yes':
                    while True:
                        user_query = input('Enter your query: ')
                        if user_query.lower() == 'exit':
                            break

                        follow_up_response = model.generate_content(f"{analysis_text}\n{user_query}")
                        print(f'{Fore.CYAN}{Style.BRIGHT}{follow_up_response.text}{Style.RESET_ALL}')
                else:
                    print(f'{Fore.YELLOW}Exiting the code analysis...{Style.RESET_ALL}')


        except Exception as e:
            print(f'{Fore.RED}Error during code analysis: {e}{Style.RESET_ALL}')
