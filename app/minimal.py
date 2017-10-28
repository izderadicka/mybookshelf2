from flask import Blueprint, render_template, request, flash, current_app, abort, redirect, url_for, Markup
from flask_login import login_required, current_user
import app.model as model
import app.logic as logic
import app.access as access
from common.utils import create_token
import os.path
import asyncio
import functools
from sqlalchemy import desc
from urllib.parse import urlencode
from engine.client import DelegatedClient
import threading

IN_UWSGI = False
try:
    import uwsgi
    import uwsgidecorators
    IN_UWSGI = True
except ImportError:
    delegated_client = None
    delegated_client_lock = threading.Lock()

bp = Blueprint('minimal', __name__)
loop = asyncio.get_event_loop()

def paginated(pg_size=24, max_pg_size=100):
    def _inner(fn):
        @functools.wraps(fn)
        def _wrap(*args, **kwargs):
            page_no = int(request.args.get('page') or 1)
            page_size = int(request.args.get('page_size') or pg_size)
            if page_size > max_pg_size:
                page_size = max_pg_size
                
            kwargs['page'] = page_no
            kwargs['page_size'] = page_size
                
            return fn(*args, **kwargs)
        return _wrap
    return _inner

@bp.route('/')
#@login_required
@paginated()
def main(page=1, page_size=24):
    ebooks=None
    if not current_user.is_anonymous and current_user.has_role('user'):
        ebooks=model.Ebook.query.order_by(desc(model.Ebook.created)).paginate(page, page_size)
        
    return render_template('main.html', ebooks=ebooks)


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
@paginated()
def search(page=1, page_size=24):
    search = ''
    ebooks = None
    if request.args.get('search'):
        search = request.args['search'].strip()

        if search:
            ebooks = logic.search_query(model.Ebook.query, search).paginate(page, page_size)
            if not ebooks.total:
                flash('No ebooks found!')

    return render_template('search.html', search=search, ebooks=ebooks,
                           additional_query = '&'+urlencode({'search':search}) if search else '')


@bp.route('/ebooks/<int:id>')
@login_required
def ebook_detail(id):
    ebook = model.Ebook.query.get(id)
    converted = logic.query_converted_sources_for_ebook(ebook.id, current_user).limit(100).all()
    return render_template('ebook.html', ebook=ebook, formats=['epub', 'mobi'], converted=converted)

@bp.route('/authors/<int:id>')
@login_required
@paginated()
def author_detail(id, page=1, page_size=24):
    author = model.Author.query.get_or_404(id)
    ebooks = author.ebooks.order_by(model.Ebook.title).paginate(page, page_size)
    return render_template('author.html', ebooks=ebooks, author=author)

@bp.route('/series/<int:id>')
@login_required
@paginated()
def series_detail(id, page=1, page_size=24):
    series = model.Series.query.get_or_404(id)
    
    ebooks = model.Ebook.query.filter(model.Ebook.series == series).order_by(model.Ebook.title).paginate(page, page_size)
    return render_template('series.html', ebooks=ebooks, series=series)



@bp.route('/ebooks/<int:id>/convert', methods=['POST'])
@access.role_required('user')
def convert_source(id):
    
    source_id = int(request.form['source_id'])
    format = request.form['format']
    # this is bit hack as user can have more roles
    role = current_user.roles[0].name
    if IN_UWSGI:
        uwsgi.mule_msg(current_user.email+'|'+ role +'|'+str(source_id)+'|'+format)
        task_id=''
    else:
        global delegated_client
        if not loop.is_running():
            abort(500, 'Event loop is not running')
        with delegated_client_lock:
            if not delegated_client or not delegated_client.is_active():
                delegated_client= DelegatedClient(current_app.config['DELEGATED_TOKEN'], 
                                                  current_app.config['DELEGATED_URI'], loop)
                
        task_id=delegated_client.call_no_wait(current_user.email, role, 'convert', source_id, format )
        
        if not task_id:
            abort(500, 'No task id')
    
    url = url_for('minimal.ebook_detail', id=id)
    flash(Markup('File was send for conversion %s- it\'ll take a while - <a href="%s">reload this page</a> later to view link to converted file' %\
                 ('' if not task_id else 'ref. %s '%task_id, url)))
    return redirect(url)

