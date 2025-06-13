from web_panel import db
from datetime import datetime
# web_panel/models.py
from web_panel.extensions import db  # ⬅️ CORRECTO

# Tu código de modelos aquí


class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con Result
    results = db.relationship('Result', backref='keyword', lazy=True)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword_id = db.Column(db.Integer, db.ForeignKey('keyword.id'), nullable=False)    
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    website = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 👈 Añadir esta línea


