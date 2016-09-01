import asyncio
import os.path
from functools import wraps, partial
from types import ModuleType


class AsyncProxy(object):
    def __init__(self, module, loop=None, executor = None):
        self._module = module
        self._loop = loop or asyncio.get_event_loop()
        self._executor = executor
        
    def __getattr__(self, name):
        function = getattr(self._module, name)
        if isinstance(function, ModuleType):
            return AsyncProxy(function)
        @wraps(function)
        async def _inner(*args,**kwargs):
            loop = kwargs.pop['loop'] if 'loop' in kwargs else self._loop 
            executor = kwargs['executor'] if 'executor' in kwargs else self._executor
            f = partial(function, *args, **kwargs)
            return await loop.run_in_executor(executor, f)
        return _inner