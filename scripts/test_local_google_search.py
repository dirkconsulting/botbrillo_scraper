from google_search import GoogleSearch

s = GoogleSearch({"engine": "google", "q": "restaurantes Bilbao", "num": 1})
print(s.get_dict().keys())
