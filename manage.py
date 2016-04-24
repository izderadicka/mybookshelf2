from flask.ext.script import Manager, prompt_pass, prompt_bool
from flask.ext.script.commands import InvalidCommand
from server import app,db
import model
from utils import hash_pwd
import marshmallow
import schema
import sys
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import or_
import os.path

manager = Manager(app)

def read_pwd():
    password=prompt_pass('Password')
    again=prompt_pass('Repeat password')
    if password!=again:
        raise InvalidCommand('Repeated password differs!')
    return password

@manager.command
def create_user(user, email, password=None):
    if not password:
        password=read_pwd()
            
    data=dict(user_name=user, email=email, password=hash_pwd(password), active=True)    
    errors=schema.UserSchema().validate(data, db.session)
    if errors:
        raise InvalidCommand('Validation Error: %s'%errors)
    
    
    u=model.User(**data)
    db.session.add(u)
    db.session.commit()

    
@manager.command
def change_password(user, password=None):
    try:    
        u=model.User.query.filter(or_(model.User.user_name == user, model.User.email == user)).one()
    except NoResultFound:
        raise InvalidCommand('No such User')
    if not password:
        password=read_pwd()
    
    u.password=hash_pwd(password)
    db.session.commit()

@manager.command
def create_tables():
    db.create_all()
    connection = db.engine.raw_connection()
    try:
        c=connection.cursor()
        script=open(os.path.join(os.path.dirname(__file__), 'data/create_ts.sql'), 'rt', encoding='utf-8-sig').read()
        
        #print(script)
        res=c.execute(script)
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