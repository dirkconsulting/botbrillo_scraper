import csv
import os
from serpapi import GoogleSearch

API_KEY = "fb9b4c73c9a61aeb089328fd74b32a5e380a2c4e0c5830281cafee15aad7997e"
KEYWORDS = [
    "restaurantes Bilbao",
    "cafeterías Madrid",
    "gimnasios Barcelona",
    "hoteles Sevilla",
]
RESULTADOS_CSV = "../resultados.csv"
MAX_RESULTADOS_POR_KEYWORD = 2

def buscar_en_serpapi(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": API_KEY,
        "num": 10
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])[:MAX_RESULTADOS_POR_KEYWORD]

def extraer_datos(result, categoria):
    title = result.get("title", "").replace(",", "")
    address = result.get("snippet", "").replace(",", "")
    link = result.get("link", "")
    phone = ""
    if "rich_snippet" in result:
        phone = result["rich_snippet"].get("top", {}).get("detected_extensions", {}).get("phone", "")
    return [categoria, title, address, phone, link]

def guardar_resultados(resultados):
    existe = os.path.exists(RESULTADOS_CSV)
    with open(RESULTADOS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["categoria", "nombre", "direccion", "telefono", "url"])
        writer.writerows(resultados)

def run_scraper():
    for keyword in KEYWORDS:
        print(f"🔍 Buscando: {keyword}")
        resultados_raw = buscar_en_serpapi(keyword)
        resultados = [extraer_datos(r, keyword) for r in resultados_raw]
        guardar_resultados(resultados)
        print(f"✅ Guardados {len(resultados)} resultados.\n")

if __name__ == "__main__":
    run_scraper()
