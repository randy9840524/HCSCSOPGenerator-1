from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import logging
from .openai_service import SOPGenerator

def generate_sop_document(sop_data):
    try:
        doc = Document()
        sop_generator = SOPGenerator()
        
        # Page setup
        sections = doc.sections
        for section in sections:
            section.page_width = Inches(8.5)
            section.page_height = Inches(11)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)

        # Basic document setup
        style = doc.styles['Normal']
        style.font.name = 'Arial'
        style.font.size = Pt(11)
        
        # Title
        title = doc.add_heading(sop_data['title'], level=1)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add spacing after title
        doc.add_paragraph()
        
        # Document info table
        info_table = doc.add_table(rows=4, cols=2)
        info_table.style = 'Table Grid'
        info_table.autofit = True
        
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
            row.cells[1].text = str(value)
            # Make label cells bold
            row.cells[0].paragraphs[0].runs[0].font.bold = True

        # Add spacing after info table
        doc.add_paragraph()

        # Generate content using OpenAI
        content = sop_generator.generate_sop_content(sop_data)
        if content:
            # Split content into sections and add them to document
            sections = content.split('\n\n')
            for section in sections:
                if section.strip():
                    para = doc.add_paragraph()
                    para.add_run(section.strip())
        
        # Add spacing before contacts
        doc.add_paragraph()
        
        # Add contacts section
        contacts_heading = doc.add_heading('Contact Information', level=2)
        contacts_heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        # IT Delivery Team Contacts
        contacts = doc.add_paragraph()
        contacts.add_run('HC IT Delivery Team\n').bold = True
        
        # Add IT contact template
        for i in range(1, 4):
            contacts.add_run(f'Contact {i}: ').bold = True
            contacts.add_run('_______________________\n')
            contacts.add_run('Role: _______________________\n')
            contacts.add_run('Email: _______________________\n')
            contacts.add_run('Phone: _______________________\n\n')
            
        # Payroll Support Contacts
        contacts.add_run('\nHCSC Payroll Support\n').bold = True
        
        # Add Payroll contact template
        for i in range(1, 4):
            contacts.add_run(f'Contact {i}: ').bold = True
            contacts.add_run('_______________________\n')
            contacts.add_run('Role: _______________________\n')
            contacts.add_run('Email: _______________________\n')
            contacts.add_run('Phone: _______________________\n\n')
            
        # Add Authorization section
        auth_heading = doc.add_heading('AUTHORISED BY:', level=2)
        auth_heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        auth = doc.add_paragraph()
        auth.add_run('Process Owner:\n').bold = True
        auth.add_run('Name & Surname: _______________________\n')
        auth.add_run('Role: _______________________\n')
        auth.add_run('Signature & date: _______________________\n\n')
        
        auth.add_run('Area Head:\n').bold = True
        auth.add_run('Name & Surname: _______________________\n')
        auth.add_run('Role: _______________________\n')
        auth.add_run('Signature & date: _______________________')

        return doc
        
    except Exception as e:
        logging.error(f"Error generating SOP document: {str(e)}")
        raise

