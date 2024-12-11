from app import db
from datetime import datetime

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_default = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Template {self.name}>'

class SOP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    document_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    effective_date = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    template = db.relationship('Template', backref=db.backref('sops', lazy=True))
    
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    payroll_email = db.Column(db.String(120))
    payroll_phone = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<SOP {self.title}>'
