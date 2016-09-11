#!/usr/bin/env python3

from flask_script import Manager, prompt_pass, prompt_bool
from flask_script.commands import InvalidCommand
from app import app, db
import app.model as model
import app.logic as logic
from common.utils import hash_pwd, purge_empty_dirs
import app.schema as schema
import sys
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import or_
import os.path
import settings
from datetime import datetime, timedelta
from traceback import print_exc


SQL_DIR = os.path.join(os.path.dirname(__file__), 'sql')

manager = Manager(app)


def read_pwd():
    password = prompt_pass('Password')
    again = prompt_pass('Repeat password')
    if password != again:
        raise InvalidCommand('Repeated password differs!')
    return password


@manager.command
def create_user(user, email, password=None, role='user'):
    if not password:
        password = read_pwd()

    data = dict(
        user_name=user, email=email, password=hash_pwd(password), active=True)
    errors = schema.UserSchema(
        exclude=('version_id',)).validate(data, db.session)
    if errors:
        raise InvalidCommand('Validation Error: %s' % errors)

    role = model.Role.query.filter_by(name=role).one()
    u = model.User(**data)
    u.roles.append(role)
    db.session.add(u)  # @UndefinedVariable
    db.session.commit()  # @UndefinedVariable


@manager.command
def change_password(user, password=None):
    try:
        u = model.User.query.filter(
            or_(model.User.user_name == user, model.User.email == user)).one()  # @UndefinedVariable
    except NoResultFound:
        raise InvalidCommand('No such User')
    if not password:
        password = read_pwd()

    u.password = hash_pwd(password)
    db.session.commit()  # @UndefinedVariable
    
    

def database_issue():
    res = db.engine.execute("select 1 from pg_extension where extname = 'unaccent'")
    if not res.fetchone():
        return 'unaccent extension missing'
    res = db.engine.execute("select 1 from pg_ts_config where cfgname = 'custom'")
    if not res.fetchone():
        return 'custom ts configuration is missing'
    
    
@manager.command
def test_database():
    issue = database_issue()
    if issue:
        print('database is not properly initialized: %s'%issue)

@manager.command
def create_tables(add_data=False, create_directories=False):
    if database_issue():
        print('Before running this command database must be initialized by superuser with these commands:\n')
        cmds = os.path.join(SQL_DIR, 'init_db.sql')
        with open(cmds, 'rt') as f:
            print(f.read())
    db.create_all()
    connection = db.engine.raw_connection()  # @UndefinedVariable
    try:
        c = connection.cursor()
        for fname in ('create_ts.sql', 'create_functions.sql'):
            script = open(os.path.join(SQL_DIR, fname), 'rt', encoding='utf-8-sig').read()
            # print(script)
            res = c.execute(script)
        connection.commit()
        if add_data:
            script = open(os.path.join(SQL_DIR, 'dump/basic.sql'), 'rt', encoding='utf-8-sig').read()
            res = c.execute(script)
            connection.commit()
            print('Default admin user with password admin was created - change it manage.py change_password admin')
    finally:
        connection.close()
        
    if create_directories:
        for d in [settings.BOOKS_BASE_DIR, settings.BOOKS_CONVERTED_DIR, settings.UPLOAD_DIR, settings.THUMBS_DIR]:
            os.makedirs(d, exist_ok=True)
        print('Created directories')


@manager.command
def update_fulltext():

    connection = db.engine.raw_connection()  # @UndefinedVariable

    try:
        c = connection.cursor()
        res = c.execute(
            "update ebook set full_text=to_tsvector('custom', ebook_full_title(id))")
        connection.commit()
    finally:
        connection.close()


@manager.command
def drop_tables():
    if prompt_bool('Are you REALLY sure? You will loose all data!'):
        db.drop_all()


@manager.command
def cleanup(uploads_older_then=24, conversions_older_then=24 * 7):
    since = datetime.now() - timedelta(hours=float(uploads_older_then))
    for upload in model.Upload.query.filter(model.Upload.created < since):
        logic.delete_upload(upload)
    db.session.commit()
    purge_empty_dirs(settings.UPLOAD_DIR, delete_root=False)
    since = datetime.now() - timedelta(hours=float(conversions_older_then))
    for conversion in model.Conversion.query.filter(model.Conversion.created < since):
        logic.delete_conversion(conversion)

    db.session.commit()
    purge_empty_dirs(settings.BOOKS_CONVERTED_DIR, delete_root=False)

    purge_empty_dirs(settings.BOOKS_BASE_DIR, delete_root=False)


if __name__ == "__main__":
    try:
        manager.run()
    except InvalidCommand as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    except Exception:
        print_exc()
        sys.exit(2)
