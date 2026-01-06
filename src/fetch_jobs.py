import requests
import os

API_KEY = os.getenv("SERP_API_KEY")

def fetch_jobs(query):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": "India",
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("jobs_results", [])