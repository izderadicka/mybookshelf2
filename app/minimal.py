from flask import Blueprint, render_template, request, flash, current_app, abort, redirect, url_for, Markup
from flask_login import login_required, current_user
import app.model as model
import app.logic as logic
import app.access as access
from common.utils import create_token
from engine.client import WAMPClient
import os.path
import asyncio

bp = Blueprint('minimal', __name__)
loop = asyncio.get_event_loop()


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
    converted = logic.query_converted_sources_for_ebook(ebook.id, current_user).limit(100).all()
    return render_template('ebook.html', ebook=ebook, formats=['epub', 'mobi'], converted=converted)

@bp.route('/ebooks/<int:id>/convert', methods=['POST'])
@access.role_required('user')
def convert_source(id):
    
    if not loop.is_running():
        abort(500, 'Event loop is not running')
    token = create_token(current_user, current_app.config['SECRET_KEY'], current_app.config['TOKEN_VALIDITY_HOURS'])
    source_id = int(request.form['source_id'])
    format = request.form['format']
    
    
    client = WAMPClient(token, current_app.config['WAMP_URI'], loop=loop)
    task_id=client.call_no_wait('convert', source_id, format )
    if not task_id:
        abort(500, 'No task id')
    client.close()
    url = url_for('minimal.ebook_detail', id=id)
    flash(Markup('File was send for conversion ref. %s- it\'ll take a while - <a href="%s">reload this page</a> later to load converted file' %\
                 (task_id, url)))
    return redirect(url)

