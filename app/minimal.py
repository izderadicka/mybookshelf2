from flask import Blueprint, render_template, request, flash, current_app, abort
from flask_login import login_required
import app.model as model
import app.logic as logic
import app.access as access
import os.path

bp = Blueprint('minimal', __name__)

@bp.route('/thumb/<int:id>')
def thumb(id):
    ebook = model.Ebook.query.get_or_404(id)
    fname = os.path.join(current_app.config['THUMBS_DIR'], '%d.jpg' % ebook.id)
    mimetype = 'image/jpeg'
    if not os.access(fname, os.R_OK):
        if ebook.cover:
            pass
        else:
            abort(404, 'No thumbnail')
    return logic.stream_response(fname, mimetype)

@bp.route('/search', methods=['GET'])
@login_required
def search():
    search = ''
    ebooks = None
    if request.args.get('search'):
        search = request.args['search'].strip()

        if search:
            ebooks = logic.search_query(model.Ebook.query, search).limit(50).all()
            if not ebooks:
                flash('No ebooks found!')

    return render_template('search.html', search=search, ebooks=ebooks)


@bp.route('/ebooks/<int:id>')
@login_required
def ebook_detail(id):
    ebook = model.Ebook.query.get(id)
    return render_template('ebook.html', ebook=ebook)

