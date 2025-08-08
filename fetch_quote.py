# fetch_quote.py
import requests
def get_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = response.json()[0] 
    print(response.json())
    # Access the first item in the list
    return data["q"], data["a"]  # 'q' is the quote, 'a' is the author
