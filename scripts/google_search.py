import requests
import os

class GoogleSearch:
    def __init__(self, params):
        self.params = params
        self.api_key = params.get("api_key") or os.getenv("SERPAPI_API_KEY")
        self.base_url = "https://serpapi.com/search"

    def get_dict(self):
        if not self.api_key:
            raise ValueError("API key is required.")
        self.params["api_key"] = self.api_key
        response = requests.get(self.base_url, params=self.params)
        response.raise_for_status()
        return response.json()
