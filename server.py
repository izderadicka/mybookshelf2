from flask import Flask, request, redirect, flash, render_template, url_for, jsonify
from model import db
from schema import schema
import sys
import decimal
from api import bp as api_bp
from flask.ext.login import LoginManager, login_user, logout_user
from utils import check_pwd, create_token

import model
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)
schema.init_app(app)
lm=LoginManager(app)

@lm.user_loader
def load_user(user_id):
    return model.User.query.get(int(user_id))

#fix for decimals
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
app.config['RESTFUL_JSON']={'default': decimal_default }

#blueprints

app.register_blueprint(api_bp, url_prefix='/api')


@app.route('/login', methods=['GET', 'POST'])
def login():
    def check_user(username, pwd):
        user= model.User.query.filter(or_(model.User.user_name == username, model.User.email ==username))\
                            .one_or_none()
        if user and check_pwd(pwd, user.password):
            return user
        
    username=""
    if request.method=='POST':
        if request.mimetype == 'application/json':
            credentials=request.get_json()
    
            if credentials and (credentials.get('email') or credentials.get('username')) and credentials.get('password'):
                q=model.User.query
                if 'username' in credentials:
                    q=q.filter(model.User.user_name == credentials['username'])
                else:
                    q=q.filter(model.User.email == credentials['email'] )
                
                try:
                    user=q.one()
                except NoResultFound:
                    return jsonify(error= 'Invalid Login')
                if not user.is_active:
                    return jsonify(error= 'Invalid Login')
                if not check_pwd(credentials['password'], user.password):
                    return jsonify(error= 'Invalid Login')
                resp= jsonify(access_token=create_token(user, app.config['SECRET_KEY'], app.config.get('TOKEN_VALIDITY_HOURS') or 4))
                #resp.headers.extend(cors_headers)
                return resp
            else:
                print (credentials)
                abort(400,'Provide credentials')
        else:
            
            user=check_user(request.form['username'], request.form['password'] )
            
            if user:
                print('Login user ', user)
                login_user(user)
                #request.args.get("next")
                return redirect('/')
            else:
                flash('Invalid user name or password!')
        
    return render_template('login.html', username=username)

@app.route('/logoff')
def logoff():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def main():
    return render_template('main.html')

if __name__ == "__main__":
    dbg=True
    host='127.0.0.1'
    if len(sys.argv)>1 and 'NO_DEBUG' in sys.argv[1:]:
        dbg=False
    if len(sys.argv)>1 and 'VISIBLE' in sys.argv[1:]:
        host='0.0.0.0'
        
    app.run(debug=dbg, host=host)

