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
        style.font.name = 'Century Gothic'
        style.font.size = Pt(10)
        
        # Update all built-in styles to use Century Gothic
        for style_name in ['Heading1', 'Heading2', 'Title']:
            if style_name in doc.styles:
                style = doc.styles[style_name]
                style.font.name = 'Century Gothic'
                style.font.size = Pt(10)
                style.font.bold = True
        
        # Title
        title = doc.add_heading(sop_data['title'], level=1)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in title.runs:
            run.font.name = 'Century Gothic'
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.underline = True
        
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
                    lines = section.strip().split('\n')
                    # Check if the line is a heading (numbered section)
                    if lines[0].strip()[0].isdigit() and '.' in lines[0]:
                        heading = doc.add_paragraph()
                        run = heading.add_run(lines[0].strip())
                        run.bold = True
                        run.underline = True
                        # Add remaining lines
                        for line in lines[1:]:
                            doc.add_paragraph(line.strip())
                    else:
                        para = doc.add_paragraph()
                        para.add_run(section.strip())
        
        # Add spacing before contacts
        doc.add_paragraph()
        
        # Add contacts section with collapsible content
        contacts_heading = doc.add_heading('Contact Information', level=2)
        contacts_heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in contacts_heading.runs:
            run.bold = True
            run.underline = True
        
        # IT Delivery Team Contacts
        contacts = doc.add_paragraph()
        team_header = contacts.add_run('HC IT Delivery Team')
        team_header.bold = True
        team_header.underline = True
        contacts.add_run(' (Click [+] to expand or [-] to collapse contacts)\n').italic = True
        
        # Add IT contact template with form fields
        contacts.add_run('\n[-] Contact 1: ').bold = True
        contacts.add_run('Veronica Nolte')
        contacts.add_run('\n    Role: _______________________')
        contacts.add_run('\n    Email: Vn@test.com')
        contacts.add_run('\n    Phone: (021) 111-111\n')
        
        # Contact 2 and 3 with XXXXX placeholders
        contacts.add_run('\n[-] Contact 2: ').bold = True
        contacts.add_run('XXXXX')
        contacts.add_run('\n    Role: _______________________')
        contacts.add_run('\n    Email: Vn@test.com')
        contacts.add_run('\n    Phone: (021) 111-112\n')
        
        contacts.add_run('\n[-] Contact 3: ').bold = True
        contacts.add_run('XXXXX')
        contacts.add_run('\n    Role: _______________________')
        contacts.add_run('\n    Email: Vn@test.com')
        contacts.add_run('\n    Phone: (021) 111-113\n')
            
        # Payroll Support Contacts
        contacts.add_run('\n')
        payroll_header = contacts.add_run('HCSC Payroll Support')
        payroll_header.bold = True
        payroll_header.underline = True
        contacts.add_run(' (Click [+] to expand or [-] to collapse contacts)\n').italic = True
        
        # Add Payroll contact template with form fields
        for i in range(1, 4):
            contacts.add_run(f'\n[-] Contact {i}: ').bold = True
            contacts.add_run('_______________________')
            contacts.add_run('\n    Role: _______________________')
            contacts.add_run('\n    Email: _______________________')
            contacts.add_run('\n    Phone: _______________________\n')
            
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

