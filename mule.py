from threading import Thread
import asyncio
import settings
from engine.client import run_loop_in_thread, WAMPClient
import uwsgi
# This is basic solution for bridging requests to WAMP in UWSGI
# It's not ideal but should be sufficient for now
# particularly recreating the client each time is inefficent - 
# 
# TODO Later I should try to come up with something smarter

loop = asyncio.get_event_loop()

def process_requests():
    while True:
        #print("Waiting for messages... yawn.")
        message = uwsgi.mule_get_msg().decode('ascii')
        token, source_id, format = message.split('|')
        source_id=int(source_id)
        client = WAMPClient(token, settings.WAMP_URI, loop=loop)
        try:
            task_id=client.call_no_wait('convert', source_id, format )
        finally:
            client.close()
        if not task_id:
            print("ERROR - no task id")
        else:
            print ("Conversion submitted", task_id)

if __name__ == '__main__':
    run_loop_in_thread(loop)
    process_requests()