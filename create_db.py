from web_panel import create_app, db
from web_panel.models import Keyword, Result

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Base de datos creada")
