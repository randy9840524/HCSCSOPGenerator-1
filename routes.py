from flask import render_template, request, send_file
from app import app, db
from models import SOP
from utils.document_generator import generate_sop_document
from datetime import datetime
import io

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_sop', methods=['POST'])
def generate_sop():
    try:
        # Extract form data
        sop_data = {
            'title': request.form['title'],
            'document_id': request.form['document_id'],
            'effective_date': datetime.strptime(request.form['effective_date'], '%Y-%m-%d'),
            'version': request.form['version'],
            'summary': request.form['summary'],
            'contact_email': request.form['contact_email'],
            'contact_phone': request.form['contact_phone'],
            'payroll_email': request.form['payroll_email'],
            'payroll_phone': request.form['payroll_phone']
        }
        
        # Create SOP record
        sop = SOP(**sop_data)
        db.session.add(sop)
        db.session.commit()
        
        # Generate document
        doc = generate_sop_document(sop_data)
        
        # Save to memory buffer
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f'SOP_{sop_data["document_id"]}.docx'
        )
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error generating SOP: {str(e)}")
        if "UNIQUE constraint failed" in str(e):
            return "A document with this ID already exists. Please try again.", 400
        return "An error occurred while generating the SOP. Please try again.", 500
