from flask import Blueprint, render_template, request, flash
from flask_login import login_required
import app.model as model
import app.logic as logic

bp=Blueprint('minimal', __name__)

@bp.route('/search', methods=['GET'])
@login_required
def search():
    search=''
    ebooks=None
    if request.args.get('search'):
        search=request.args['search'].strip()
        
        if search:
            ebooks=logic.search_query(model.Ebook.query, search).limit(50).all()
            if not ebooks:
                flash('No ebooks found!')
            
    
    return render_template('search.html', search=search, ebooks=ebooks)

@bp.route('/ebooks/<int:id>')
@login_required
def ebook_detail(id):
    ebook=model.Ebook.query.get(id)
    return render_template('ebook.html', ebook=ebook)

@bp.route('/download/<int:id>')
@login_required
def download(id):
    return logic.download(id)