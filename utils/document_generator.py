from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from .openai_service import SOPGenerator

def generate_sop_document(sop_data):
    doc = Document()
    sop_generator = SOPGenerator()
    
    # Basic document setup
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(11)
    
    # Title
    header = doc.add_heading(sop_data['title'], level=1)
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Document info
    info_table = doc.add_table(rows=4, cols=2)
    info_table.style = 'Table Grid'
    
    # Add document info
    info = [
        ('Document ID:', sop_data['document_id']),
        ('Effective Date:', sop_data['effective_date'].strftime('%m/%d/%Y')),
        ('Version:', sop_data['version']),
        ('Created:', datetime.now().strftime('%m/%d/%Y'))
    ]
    for i, (label, value) in enumerate(info):
        row = info_table.rows[i]
        row.cells[0].text = label
        row.cells[1].text = value

    # Generate content using OpenAI
    content = sop_generator.generate_sop_content(sop_data)
    if content:
        doc.add_paragraph(content)
    
    # Add contacts
    doc.add_heading('Contact Information', level=2)
    contacts = doc.add_paragraph()
    contacts.add_run('HC IT Delivery Team\n').bold = True
    contacts.add_run(f'Email: {sop_data["contact_email"]}\nPhone: {sop_data["contact_phone"]}\n\n')
    contacts.add_run('HCSC Payroll Support\n').bold = True
    contacts.add_run(f'Email: {sop_data["payroll_email"]}\nPhone: {sop_data["payroll_phone"]}')
    
    return doc

