from app import db
from datetime import datetime

class SOP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    document_id = db.Column(db.String(50), unique=True, nullable=False)
    effective_date = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    payroll_email = db.Column(db.String(120))
    payroll_phone = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<SOP {self.title}>'
