from dotenv import load_dotenv
import os

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

# Clustering config
N_CLUSTERS = 5
MAX_POSTS = 100

# Association rules config
MIN_SUPPORT = 0.1
MIN_CONFIDENCE = 0.5