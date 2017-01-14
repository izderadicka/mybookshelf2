from flask import request, redirect, flash, render_template, url_for, jsonify, Blueprint, abort,\
    current_app
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from functools import wraps
from common.utils import check_pwd, create_token, create_refresh_token, verify_token
import app.model as model
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
import logging
from app.cors import cors_enabled
import re

logger = logging.getLogger('access')


bp = Blueprint('access', __name__)
lm = LoginManager()


SECRET_KEY = ''
TOKEN_VALIDITY_HOURS = 4


@bp.record_once
def on_load(state):
    global SECRET_KEY, TOKEN_VALIDITY_HOURS
    lm.init_app(state.app)
    SECRET_KEY = state.app.config.get('SECRET_KEY')
    TOKEN_VALIDITY_HOURS = state.app.config.get('TOKEN_VALIDITY_HOURS')


@lm.request_loader
def load_user_from_request(request):
    user_token = request.args.get('bearer_token')
    if not user_token:
        token = request.headers.get('Authorization')
        if token and token.lower().startswith('bearer '):
            user_token = token[7:].strip()
    if not user_token:
        return

    claim = verify_token(user_token, SECRET_KEY)
    if claim:
        user = model.User.query.get(claim['id'])  # @UndefinedVariable
        if user and user.is_active:
            return user

    # finally, return None if both methods did not login the user
    return None


@lm.user_loader
def load_user(user_id):
    return model.User.query.get(int(user_id))  # @UndefinedVariable


def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            user = current_user
            if not(user.is_authenticated and user.has_role(*roles)):
                abort(401, 'Access denied')
            return fn(*args, **kwargs)
        return inner
    return wrapper


def role_required_owning(*roles, if_own=None, owning_role=None):
    assert roles or (if_own and owning_role)
    user = current_user
    if user.is_authenticated and user.has_role(*roles):
        return
    if if_own and if_own.created_by == user and user.is_authenticated and user.has_role(owning_role):
        return
    abort(403, 'Access denied')


def can_change_object(obj):
    return role_required_owning('superuser', if_own=obj, owning_role='user')


def can_delete_object(obj):
    return role_required_owning('superuser', if_own=obj, owning_role='user')

@bp.route('/login', methods=['GET', 'POST'])
@cors_enabled
def login():
    def check_user(username, pwd):
        user = model.User.query.filter(or_(model.User.user_name == username,  # @UndefinedVariable
                                           model.User.email == username)).one_or_none()  # @UndefinedVariable
        if user and check_pwd(pwd, user.password):
            return user

    username = ""
    if request.method == 'POST':
        if request.mimetype == 'application/json':
            credentials = request.get_json()

            if credentials and (credentials.get('email') or credentials.get('username')) and\
                    credentials.get('password'):
                q = model.User.query
                if 'username' in credentials:
                    q = q.filter(
                        model.User.user_name == credentials['username'])
                else:
                    q = q.filter(model.User.email == credentials['email'])

                try:
                    user = q.one()
                except NoResultFound:
                    return jsonify(error='Invalid Login')
                if not user.is_active:
                    return jsonify(error='Invalid Login')
                if not check_pwd(credentials['password'], user.password):
                    return jsonify(error='Invalid Login')
                resp = jsonify(
                    access_token=create_token(user, SECRET_KEY, TOKEN_VALIDITY_HOURS or 4),
                    refresh_token = create_refresh_token(user, 
                                                         current_app.config['SECRET_KEY2'], 
                                                         current_app.config['TOKEN_REFRESH_HOURS']))
                # resp.headers.extend(cors_headers)
                return resp
            elif credentials and credentials.get('refresh_token'):
                header = request.headers.get('Authorization')
                if not header:
                    abort(400, 'Need authorization header to refresh token')
                m = re.match(r'Bearer\s+(.+)', header, re.IGNORECASE)
                if not m:
                    abort(400, 'Invalid authorization header')
                token = m.group(1)
                claim = verify_token(token,  SECRET_KEY, validate_expiration=False)
                if not claim:
                    abort(400, 'Invalid token')
                    
                user_id = claim['id']
                refresh_claim = verify_token(credentials['refresh_token'], current_app.config['SECRET_KEY2'])
                if not refresh_claim:
                    abort(400, 'Invalid refresh token')
                    
                if not user_id == refresh_claim['id']:
                    abort(400, 'Inconsistent tokens')
                    
                user = model.User.query.get(user_id)
                if not user:
                    return jsonify(error='Invalid Login')
                
                return jsonify(
                    access_token=create_token(user, SECRET_KEY, TOKEN_VALIDITY_HOURS or 4))
                
                
            else:
                logger.info('Failed JSON login with %s', credentials)
                abort(400, 'Provide credentials')
        else:

            user = check_user(
                request.form['username'], request.form['password'])

            if user:
                remember_me = request.form.get('rememberme')
                logger.info('User logged in %s , remember me is %s', user.user_name, remember_me)
                login_user(user, remember=remember_me)
                # request.args.get("next")
                return redirect('/')
            else:
                flash('Invalid user name or password!')

    return render_template('login.html', username=username)


@bp.route('/logoff')
@login_required
def logoff():
    logout_user()
    return redirect(url_for('access.login'))
