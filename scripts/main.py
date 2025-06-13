import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from web_panel import create_app
from web_panel.models import db, Keyword, Result
from serpapi.google_search import GoogleSearch
from tqdm import tqdm

def buscar_negocios_google_maps(keyword):
    params = {
        "engine": "google_maps",
        "q": keyword,
        "api_key": os.getenv("SERPAPI_KEY"),
        "hl": "es",
        "google_domain": "google.es",
        "type": "search"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    negocios = []
    for r in results.get("local_results", []):
        negocios.append({
            "name": r.get("title", ""),
            "address": r.get("address", ""),
            "phone": r.get("phone", ""),
            "website": r.get("website", ""),
        })

    return negocios

def main():
    keywords = Keyword.query.all()
    for k in tqdm(keywords, desc="📍 Scrapeando Google Maps"):
        negocios = buscar_negocios_google_maps(k.keyword)
        for n in negocios:
            if not Result.query.filter_by(phone=n["phone"]).first():
                r = Result(
                    keyword_id=k.id,
                    name=n["name"],
                    address=n["address"],
                    phone=n["phone"],
                    website=n["website"]
                )
                db.session.add(r)
        db.session.commit()
    print("✅ Scraping de Google Maps terminado.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        main()
