# Author: Hareesh Kumar Gajulapalli
import os
import sys
from dotenv import load_dotenv

class AppConfigError(Exception):
    pass

class Config:
    def __init__(self):
        # Load .env file
        load_dotenv() 

        # Using default value even if not present
        self.FLASK_APP = os.getenv("FLASK_APP", "app.py")
        self.FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == 'true'
        
        self.SECRET_KEY = self._get_env_var("SECRET_KEY")
        self.GOOGLE_CLIENT_ID = self._get_env_var("GOOGLE_CLIENT_ID")
        self.GOOGLE_CLIENT_SECRET = self._get_env_var("GOOGLE_CLIENT_SECRET")

        # Extra validation as I want secret key to be longer than 15 characters.
        if len(self.SECRET_KEY) < 16:
            raise AppConfigError("SECRET_KEY must be at least 16 characters long.")

    def _get_env_var(self, var_name: str, default=None):
        value = os.getenv(var_name, default)
        if value is None:
            print(f"Error: Missing required environment variable: {var_name}")
            print("Please set this variable before starting the application.")
            raise AppConfigError(f"Missing required environment variable: {var_name}")
        return value

# Instantiate the config once
try:
    config = Config()
except AppConfigError as e:
    print(f"Configuration Error: {e}")
    sys.exit(1)