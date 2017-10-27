#! /usr/bin/env python3

import sys
import asyncio
#from engine.client import run_loop_in_thread
from app import app


if __name__ == "__main__":
    dbg=True
    host='127.0.0.1'
    if len(sys.argv)>1 and 'NO_DEBUG' in sys.argv[1:]:
        dbg=False
    if len(sys.argv)>1 and 'VISIBLE' in sys.argv[1:]:
        host='0.0.0.0'
    loop = asyncio.get_event_loop()
    #run_loop_in_thread(loop)   
    app.run(debug=dbg, host=host, port=6006)

