from app import db
from datetime import datetime

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
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
    template = db.relationship('Template', backref='sops')
    
    # IT Delivery Team Contacts
    it_team_name = db.Column(db.String(200), default="HC IT Delivery Team")
    it_contact1_name = db.Column(db.String(100))
    it_contact1_role = db.Column(db.String(100))
    it_contact1_email = db.Column(db.String(120))
    it_contact1_phone = db.Column(db.String(20))
    it_contact2_name = db.Column(db.String(100))
    it_contact2_role = db.Column(db.String(100))
    it_contact2_email = db.Column(db.String(120))
    it_contact2_phone = db.Column(db.String(20))
    it_contact3_name = db.Column(db.String(100))
    it_contact3_role = db.Column(db.String(100))
    it_contact3_email = db.Column(db.String(120))
    it_contact3_phone = db.Column(db.String(20))
    
    # Payroll Support Contacts
    payroll_team_name = db.Column(db.String(200), default="HCSC Payroll Support")
    payroll_contact1_name = db.Column(db.String(100))
    payroll_contact1_role = db.Column(db.String(100))
    payroll_contact1_email = db.Column(db.String(120))
    payroll_contact1_phone = db.Column(db.String(20))
    payroll_contact2_name = db.Column(db.String(100))
    payroll_contact2_role = db.Column(db.String(100))
    payroll_contact2_email = db.Column(db.String(120))
    payroll_contact2_phone = db.Column(db.String(20))
    payroll_contact3_name = db.Column(db.String(100))
    payroll_contact3_role = db.Column(db.String(100))
    payroll_contact3_email = db.Column(db.String(120))
    payroll_contact3_phone = db.Column(db.String(20))
    
    # Authorization
    process_owner_name = db.Column(db.String(100))
    process_owner_role = db.Column(db.String(100))
    area_head_name = db.Column(db.String(100))
    area_head_role = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<SOP {self.title}>'
