import os
from dotenv import load_dotenv

load_dotenv()  # loads .env

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
