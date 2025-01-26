import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key_123")

# For Vercel, use SQLite in /tmp directory since that's writable
db_path = '/tmp/sop.db' if os.environ.get('VERCEL') else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance/sop.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Import routes after db initialization
from routes import *

# Create database tables
def init_db():
    with app.app_context():
        try:
            db.create_all()
            
            # Create default template if it doesn't exist
            from models import Template
            if not Template.query.filter_by(is_default=True).first():
                default_template = Template(
                    name="ISO 9000 Standard Template",
                    content="1. Purpose\n2. Scope\n3. Definitions\n4. Responsibilities\n5. Procedure\n6. References\n7. Records\n8. Quality Records\n9. Revision History",
                    is_default=True
                )
                db.session.add(default_template)
                db.session.commit()
                logger.info("Default template created successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
