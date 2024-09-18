import requests
import urllib.parse
from g4f.client import Client

client = Client()

def search_news(query):
    search_engine_url = "https://news.google.com/search?q="
    search_query = urllib.parse.quote(query)
    full_url = search_engine_url + search_query
    return full_url


def get_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def get_top_news():
    api_key = '84b2584f4b9cf3a0f5d1d01e2678841a'  # Replace with your actual API key
    api_url = 'https://gnews.io/api/v4/top-headlines'
    params = {
        'apikey': api_key,
        'lang': 'en',
        'country': '*',
        'max': 10
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        return [{'title': article['title'], 'source': article['source']['name'], 'publishedAt': article['publishedAt'], 'url': article['url']} for article in articles]
    else:
        return []

def get_top_news_for_india():
    api_key = '84b2584f4b9cf3a0f5d1d01e2678841a'  # Replace with your actual API key
    api_url = 'https://gnews.io/api/v4/top-headlines'
    params = {
        'apikey': api_key,
        'lang': 'en',
        'country': 'in',
        'max': 10
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        return [{'title': article['title'], 'source': article['source']['name'], 'publishedAt': article['publishedAt'], 'url': article['url']} for article in articles]
    else:
        return []

def check_url_safety(api_key, url):
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {"clientId": "your_project_name", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        response = requests.post(api_url, json=payload)
        response_data = response.json()
        if "matches" in response_data:
            return "Unsafe: The URL is flagged by Safe Browsing."
        else:
            return "Safe: No threats found for the URL."
    except Exception as e:
        return f"An error occurred: {e}"