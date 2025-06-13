from serpapi import GoogleSearch
import os

params = {
    "engine": "google",
    "q": "restaurantes bilbao",
    "location": "Bilbao, Spain",
    "google_domain": "google.es",
    "gl": "es",
    "hl": "es",
    "api_key": os.getenv("SERPAPI_KEY")
}

search = GoogleSearch(params)
results = search.get_dict()

print(results.keys())
