import os
import requests
import json

API_KEY = os.getenv("SERP_API_KEY")

if not API_KEY:
    raise Exception("SERP_API_KEY not found. Did you restart Terminal?")

params = {
    "engine": "google_jobs",
    "q": "Solutions Consultant",
    "location": "India",
    "api_key": API_KEY
}

response = requests.get("https://serpapi.com/search", params=params)
response.raise_for_status()

data = response.json()

# print("\n=== FULL RESPONSE KEYS ===")
# print(data.keys())

# print("\n=== RAW RESPONSE (first 1000 chars) ===")
# print(json.dumps(data, indent=2)[:1000])

jobs = data.get("jobs_results", [])

# print(f"\nParsed jobs_results count: {len(jobs)}")

jobs = response.json().get("jobs_results", [])

print(f"\nFound {len(jobs)} jobs\n")

for i, job in enumerate(jobs[:5], start=1):  # print only first 5
    print(f"{i}. {job.get('title')}")
    print(f"   Company: {job.get('company_name')}")
    print(f"   Link: {job.get('link')}\n")