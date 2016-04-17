from flask import Flask, request
from model import db
import sys
import decimal
from api import bp as api_bp

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)

#fix for decimals
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
app.config['RESTFUL_JSON']={'default': decimal_default }

#blueprints

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == "__main__":
    dbg=True
    host='127.0.0.1'
    if len(sys.argv)>1 and 'NO_DEBUG' in sys.argv[1:]:
        dbg=False
    if len(sys.argv)>1 and 'VISIBLE' in sys.argv[1:]:
        host='0.0.0.0'
        
    app.run(debug=dbg, host=host)

