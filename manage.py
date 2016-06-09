#!/usr/bin/env python

from flask_script import Manager, prompt_pass, prompt_bool
from flask_script.commands import InvalidCommand
from app import app,db
import app.model as model
from app.utils import hash_pwd
import app.schema as schema
import sys
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import or_
import os.path


DATA_DIR='./app/data'

manager = Manager(app)


def read_pwd():
    password=prompt_pass('Password')
    again=prompt_pass('Repeat password')
    if password!=again:
        raise InvalidCommand('Repeated password differs!')
    return password

@manager.command
def create_user(user, email, password=None, role='user'):
    if not password:
        password=read_pwd()
            
    data=dict(user_name=user, email=email, password=hash_pwd(password), active=True)    
    errors=schema.UserSchema(exclude=('version_id',)).validate(data, db.session)
    if errors:
        raise InvalidCommand('Validation Error: %s'%errors)
    
    role=model.Role.query.filter_by(name=role).one()
    u=model.User(**data)
    u.roles.append(role)
    db.session.add(u)  # @UndefinedVariable
    db.session.commit()  # @UndefinedVariable

    
@manager.command
def change_password(user, password=None):
    try:    
        u=model.User.query.filter(or_(model.User.user_name == user, model.User.email == user)).one()  # @UndefinedVariable
    except NoResultFound:
        raise InvalidCommand('No such User')
    if not password:
        password=read_pwd()
    
    u.password=hash_pwd(password)
    db.session.commit()  # @UndefinedVariable

@manager.command
def create_tables():
    db.create_all()
    connection = db.engine.raw_connection()  # @UndefinedVariable
    try:
        c=connection.cursor()
        for fname in ('create_ts.sql', 'create_functions.sql'):
            script=open(os.path.join(os.path.dirname(__file__), DATA_DIR, fname), 'rt', encoding='utf-8-sig').read()
            #print(script)
            res=c.execute(script)
        connection.commit()
    finally:
        connection.close()
        
@manager.command
def update_fulltext():
    
    connection = db.engine.raw_connection()  # @UndefinedVariable
    
    try:
        c=connection.cursor()
        res=c.execute("update ebook set full_text=to_tsvector('custom', ebook_full_title(id))")
        connection.commit()
    finally:
        connection.close()
    
    # 
@manager.command    
def drop_tables():
    if prompt_bool('Are you REALLY sure? You will loose all data!'):
        db.drop_all()   

if __name__ == "__main__":
    try:
        manager.run()
    except InvalidCommand as err:
        print(err, file=sys.stderr)
        sys.exit(1)