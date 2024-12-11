from flask import Blueprint, render_template, request, send_file
from app import db, logger
from models import SOP
from utils.document_generator import generate_sop_document
from datetime import datetime
import io

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate_sop', methods=['POST'])
def generate_sop():
    sop_data = None
    try:
        # Extract form data
        sop_data = {
            'title': request.form['title'].strip(),
            'document_id': request.form['document_id'].strip(),
            'effective_date': datetime.strptime(request.form['effective_date'], '%Y-%m-%d'),
            'version': request.form['version'].strip(),
            'summary': request.form['summary'].strip(),
            'contact_email': request.form['contact_email'].strip(),
            'contact_phone': request.form['contact_phone'].strip(),
            'payroll_email': request.form['payroll_email'].strip(),
            'payroll_phone': request.form['payroll_phone'].strip()
        }
        
        logger.info(f"Attempting to create SOP with document ID: {sop_data['document_id']}")
        
        # Use a transaction to handle race conditions
        try:
            # Check if document ID already exists within transaction
            existing_sop = db.session.query(SOP).filter_by(
                document_id=sop_data['document_id']
            ).with_for_update().first()
            
            if existing_sop:
                db.session.rollback()
                logger.warning(f"Document ID already exists: {sop_data['document_id']}")
                return "A document with this ID already exists. Please try generating a new document ID.", 400
                
            # Create SOP record
            sop = SOP(**sop_data)
            db.session.add(sop)
            db.session.commit()
            logger.info(f"Successfully created SOP with document ID: {sop_data['document_id']}")
        
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
            if "UNIQUE constraint failed" in str(e):
                return "A document with this ID already exists. Please try again.", 400
            raise
            
    except Exception as e:
        logger.error(f"Error generating SOP: {str(e)}")
        if sop_data and 'document_id' in sop_data:
            logger.error(f"Document ID: {sop_data['document_id']}")
        logger.error(f"Full error details: {repr(e)}")
        return "An error occurred while generating the SOP. Please try again.", 500
