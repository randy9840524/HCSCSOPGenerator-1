import os
import openai
from datetime import datetime

class SOPGenerator:
    def __init__(self):
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        
    def generate_sop_content(self, sop_data):
        prompt = f"""
        Generate a detailed Standard Operating Procedure (SOP) that is ISO 9000 compliant based on the following summary:

        Title: {sop_data['title']}
        Summary: {sop_data['summary']}

        The SOP should include:
        1. Purpose
        2. Scope
        3. Definitions
        4. Responsibilities
        5. Procedure
        6. References
        7. Records
        8. Quality Records
        9. Revision History

        Format the response in a clear, professional manner suitable for a business document.
        Focus on clarity, completeness, and compliance with ISO 9000 standards.
        """

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are SOP Generator Pro, an expert in creating ISO 9000 compliant Standard Operating Procedures."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating SOP content: {str(e)}")
            return None
