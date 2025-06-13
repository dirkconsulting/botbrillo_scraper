import os
from google_search import GoogleSearch  # Lo importamos directamente del archivo local

# Configura la API key de SerpApi (opción 1: variable de entorno)
os.environ["SERPAPI_KEY"] = "fb9b4c73c9a61aeb089328fd74b32a5e380a2c4e0c5830281cafee15aad7997e"

params = {
    "engine": "google",
    "q": "restaurantes en Bilbao",
    "location": "Bilbao, Spain",
    "google_domain": "google.com",
    "hl": "es",
    "gl": "es"
}

search = GoogleSearch(params)
results = search.get_dict()

print("🔍 Resultados disponibles:")
print(results.keys())
