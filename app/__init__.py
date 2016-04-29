from flask import Flask, render_template
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
import decimal

app = Flask(__name__)
app.config.from_object('settings')
db=SQLAlchemy(app)


#fix for decimals
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
app.config['RESTFUL_JSON']={'default': decimal_default }

@app.route('/')
#@login_required
def main():
    return render_template('main.html')



#blueprints
def register_blueprints():
    from app.api import bp as api_bp
    from app.access import bp as access_bp
    from app.minimal import bp as minimal_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(access_bp)
    app.register_blueprint(minimal_bp)
    
register_blueprints()