from flask import Flask
from flask_migrate import Migrate
from web_panel import create_app
from web_panel.models import db

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


import subprocess
from flask import Blueprint, redirect, url_for, flash

main = Blueprint('main', __name__)

@main.route('/run-scraper', methods=['POST'])
def run_scraper():
    try:
        subprocess.Popen(["python3", "scraper.py"], cwd="/root/botbrillo_scraper")
        flash("✅ Scraper iniciado correctamente", "success")
    except Exception as e:
        flash(f"❌ Error al iniciar el scraper: {e}", "danger")
    return redirect(url_for('main.index'))  # Ajusta si tu ruta principal se llama distinto
