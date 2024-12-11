from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from .openai_service import SOPGenerator

def generate_sop_document(sop_data):
    doc = Document()
    sop_generator = SOPGenerator()
    
    # Document formatting
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(11)
    
    # Header
    header = doc.add_heading('', level=1)
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header.add_run(sop_data['title']).bold = True
    
    # Document info table
    table = doc.add_table(rows=4, cols=2)
    table.style = 'Table Grid'
    
    cells = [
        ('Document ID:', sop_data['document_id']),
        ('Effective Date:', sop_data['effective_date'].strftime('%m/%d/%Y')),
        ('Version:', sop_data['version']),
        ('Created:', datetime.now().strftime('%m/%d/%Y'))
    ]
    
    for i, (label, value) in enumerate(cells):
        row = table.rows[i]
        row.cells[0].text = label
        row.cells[1].text = value

    # Generate SOP content using GPT
    generated_content = sop_generator.generate_sop_content(sop_data)
    if generated_content:
        # Add generated content sections
        doc.add_paragraph(generated_content)
    
    # Contact Information
    doc.add_heading('Contact Information', level=2)
    contacts = doc.add_paragraph()
    contacts.add_run('HC IT Delivery Team\n').bold = True
    contacts.add_run(f'Email: {sop_data["contact_email"]}\n')
    contacts.add_run(f'Phone: {sop_data["contact_phone"]}\n\n')
    contacts.add_run('HCSC Payroll Support\n').bold = True
    contacts.add_run(f'Email: {sop_data["payroll_email"]}\n')
    contacts.add_run(f'Phone: {sop_data["payroll_phone"]}')
    
    # Approval section
    doc.add_heading('Approval', level=2)
    approval_table = doc.add_table(rows=4, cols=4)
    approval_table.style = 'Table Grid'
    
    # Header row
    header_cells = approval_table.rows[0].cells
    for i, header in enumerate(['Name', 'Title', 'Department', 'Date']):
        header_cells[i].text = header
        
    # Default approval row for Cindy Williams
    approval_row = approval_table.rows[1].cells
    approval_row[0].text = "Cindy Williams"
    approval_row[1].text = "Payroll Support"
    approval_row[2].text = "HCSC Payroll Support"
    approval_row[3].text = datetime.now().strftime('%m/%d/%Y')
    
    return doc

