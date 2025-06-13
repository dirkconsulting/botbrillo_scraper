import os
import csv
from serpapi import GoogleSearch

API_KEY = "fb9b4c73c9a61aeb089328fd74b32a5e380a2c4e0c5830281cafee15aad7997e"  # Reemplaza con tu clave real de SerpApi

KEYWORDS_FILE = "keywords.txt"
RESULTS_FILE = "resultados.csv"

AGREGADORES = [
    "tripadvisor", "booking", "trivago", "yelp", "thefork", "groupon",
    "expedia", "viator", "hotels.com", "verybilbao", "elle.com", "facebook",
    "instagram", "wikiloc", "pinterest"
]

def cargar_keywords():
    with open(KEYWORDS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def es_web_valida(url):
    if not url:
        return False
    for dominio in AGREGADORES:
        if dominio in url.lower():
            return False
    return True

def buscar_negocios(keyword):
    params = {
        "engine": "google_maps",
        "q": keyword,
        "type": "search",
        "hl": "es",
        "gl": "es",
        "api_key": API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    negocios = []
    if "local_results" in results:
        for result in results["local_results"]:
            url = result.get("website")
            if es_web_valida(url):
                negocios.append({
                    "categoria": keyword,
                    "nombre": result.get("title"),
                    "direccion": result.get("address"),
                    "telefono": result.get("phone_number", ""),
                    "url": url
                })
                if len(negocios) >= 2:  # Limita resultados por keyword
                    break
    return negocios

def guardar_resultados(datos):
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["categoria", "nombre", "direccion", "telefono", "url"])
        writer.writeheader()
        writer.writerows(datos)

def main():
    keywords = cargar_keywords()
    todos_los_resultados = []

    for keyword in keywords:
        print(f"🔍 Buscando: {keyword}")
        resultados = buscar_negocios(keyword)
        todos_los_resultados.extend(resultados)

    guardar_resultados(todos_los_resultados)
    print(f"✅ Resultados guardados en {RESULTS_FILE}")

if __name__ == "__main__":
    main()
