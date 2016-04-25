from flask import Flask
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


#blueprints
def register_blueprints():
    from app.api import bp as api_bp
    from app.access import bp as access_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(access_bp)
    
register_blueprints()