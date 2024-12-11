from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models import Template

templates = Blueprint('templates', __name__)

@templates.route('/templates')
def list_templates():
    templates = Template.query.all()
    return render_template('templates/list.html', templates=templates)

@templates.route('/templates/new', methods=['GET', 'POST'])
def new_template():
    if request.method == 'POST':
        template = Template(
            name=request.form['name'],
            description=request.form['description'],
            content=request.form['content'],
            is_default=request.form.get('is_default', False)
        )
        
        if template.is_default:
            # Ensure only one default template
            Template.query.filter_by(is_default=True).update({'is_default': False})
        
        db.session.add(template)
        db.session.commit()
        return redirect(url_for('templates.list_templates'))
    
    return render_template('templates/new.html')

@templates.route('/templates/<int:id>/edit', methods=['GET', 'POST'])
def edit_template(id):
    template = Template.query.get_or_404(id)
    
    if request.method == 'POST':
        template.name = request.form['name']
        template.description = request.form['description']
        template.content = request.form['content']
        template.is_default = request.form.get('is_default', False)
        
        if template.is_default:
            Template.query.filter(Template.id != id).update({'is_default': False})
        
        db.session.commit()
        return redirect(url_for('templates.list_templates'))
    
    return render_template('templates/edit.html', template=template)
