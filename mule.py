from threading import Thread
import asyncio
import settings
from engine.client import run_loop_in_thread, DelegatedClient
import uwsgi
import traceback
# This is basic solution for bridging requests to WAMP in UWSGI
# It's not ideal but should be sufficient for now
# particularly recreating the client each time is inefficent - 
# 
# TODO Later I should try to come up with something smarter

loop = asyncio.get_event_loop()

def process_requests():
    delegated_client = None

    while True:
        #print("Waiting for messages... yawn.")
        message = uwsgi.mule_get_msg().decode('ascii')
        user,role, source_id, format = message.split('|')
        source_id=int(source_id)
        try:
            if not delegated_client or not delegated_client.is_active():
                delegated_client= DelegatedClient(settings.DELEGATED_TOKEN, 
                                                  settings.DELEGATED_URI, loop)
        
            task_id=delegated_client.call_no_wait(user, role, 'convert', source_id, format )
        except Exception:
            traceback.print_exc()
        else:
            print ("Conversion submitted", task_id)

if __name__ == '__main__':
    run_loop_in_thread(loop)
    process_requests()