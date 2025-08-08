# find_image.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def search_image(keywords):
    headers = {"Authorization": PEXELS_API_KEY}
    query = "+".join(keywords)
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["photos"][0]["src"]["medium"]
