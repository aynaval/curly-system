import os
import yaml
from dotenv import load_dotenv

def load_config(file_path: str):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    # Load environment variables from .env file
    load_dotenv()

    # Update config with environment variables
    config['watsonxai']['api_key'] = os.getenv('WX_AI_API_KEY')
    config['watsonxai']['project_id'] = os.getenv('WX_AI_PROJECT_ID')
    return config

file_path = 'conf/config.yaml'
config = load_config(file_path)