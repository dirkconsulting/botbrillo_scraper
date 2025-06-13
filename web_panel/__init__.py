from flask import Flask
from web_panel.extensions import db  # ✅ import correcto
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'clave_super_secreta_123'

    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'scraper.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    db.init_app(app)

    # Manejo de errores
    @app.errorhandler(Exception)
    def handle_exception(e):
        return f"<pre>{str(e)}</pre>", 500

    from web_panel.routes import panel as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
