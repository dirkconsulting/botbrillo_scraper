from flask import Blueprint, render_template, redirect, url_for, flash, send_file, request
from web_panel.models import db, Keyword, Result
from sqlalchemy import desc
import csv
import io
from scripts.main import main  # Asegúrate de que este import funciona

panel = Blueprint('panel', __name__)

@panel.route('/')
def index():
    keywords = Keyword.query.order_by(desc(Keyword.created_at)).all()
    return render_template('index.html', keywords=keywords)

@panel.route('/resultados')
def resultados():
    page = request.args.get('page', 1, type=int)
    resultados = Result.query.order_by(desc(Result.created_at)).paginate(page=page, per_page=25)
    return render_template('resultados.html', resultados=resultados)

@panel.route('/iniciar-scraper')
def iniciar_scraper():
    try:
        main()
        flash("✅ Scraper ejecutado correctamente", "success")
    except Exception as e:
        flash(f"❌ Error al ejecutar scraper: {str(e)}", "danger")
    return redirect(url_for('panel.index'))

@panel.route('/exportar-resultados')
def exportar_resultados():
    resultados = Result.query.order_by(Result.created_at.desc()).all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Keyword', 'Título', 'Teléfono', 'Web', 'Fecha'])
    for r in resultados:
        cw.writerow([r.keyword.keyword, r.title, r.phone, r.website, r.created_at])
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name="resultados.csv")
