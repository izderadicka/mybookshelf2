#! /usr/bin/env python

from flask import render_template
import sys
from app import app
from app.access import lm
from flask_login import login_required

app.config.from_object('settings')

@app.route('/')
#@login_required
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

