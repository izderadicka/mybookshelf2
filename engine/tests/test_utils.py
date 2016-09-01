from unittest import TestCase
import asyncio
import os
from engine.utils import AsyncProxy


class TestAsyncProxy(TestCase):
    def test(self):
        loop = asyncio.get_event_loop()
        async_os = AsyncProxy(os)
        x = loop.run_until_complete(async_os.stat(__file__))
        self.assertTrue(x.st_size> 100)
        self.assertEqual(async_os.stat.__name__, 'stat')
        
        self.assertTrue(loop.run_until_complete(async_os.path.exists(__file__)))
        
        with self.assertRaises(AttributeError):
            async_os.xxx('yyy')
        
        
        