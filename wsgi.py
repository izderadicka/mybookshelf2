import asyncio
from engine.client import run_loop_in_thread
from app import app
from uwsgidecorators import postfork

loop = asyncio.get_event_loop()
@postfork
def start_loop():
    run_loop_in_thread(loop)



loop = asyncio.get_event_loop()
#run_loop_in_thread(loop)

