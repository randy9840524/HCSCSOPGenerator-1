import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key_123")

# Ensure instance folder exists
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)
    logger.info(f"Created instance directory at {instance_path}")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(instance_path, 'sop.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Import routes after db initialization
from routes import *

# Create database tables
with app.app_context():
    try:
        # Recreate all tables
        db.drop_all()
        db.create_all()
        
        # Create default template
        from models import Template
        default_template = Template(
            name="ISO 9000 Standard Template",
            content="1. Purpose\n2. Scope\n3. Definitions\n4. Responsibilities\n5. Procedure\n6. References\n7. Records\n8. Quality Records\n9. Revision History",
            is_default=True
        )
        db.session.add(default_template)
        db.session.commit()
        logger.info("Database tables recreated successfully and default template created")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
