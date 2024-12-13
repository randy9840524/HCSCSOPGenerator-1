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
        
        contacts = doc.add_paragraph()
        contacts.add_run('HC IT Delivery Team\n').bold = True
        contacts.add_run(f'Email: {sop_data["contact_email"]}\n')
        contacts.add_run(f'Phone: {sop_data["contact_phone"]}\n\n')
        contacts.add_run('HCSC Payroll Support\n').bold = True
        contacts.add_run(f'Email: {sop_data["payroll_email"]}\n')
        contacts.add_run(f'Phone: {sop_data["payroll_phone"]}')

        return doc
        
    except Exception as e:
        logging.error(f"Error generating SOP document: {str(e)}")
        raise

