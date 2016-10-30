import os
from inspect import isclass
import importlib
import cli.actions as plugins

class ActionError(Exception):
    pass

class SoftActionError(ActionError):
    pass


class Action():
    DESCRIPTION = ""

    @classmethod
    def create_arguments_parser(cls, subparsers):
        parser = subparsers.add_parser(cls.__name__.lower(), help=cls.DESCRIPTION)
        cls.add_arguments(parser)
        return parser

    @staticmethod
    def add_arguments(parser):
        pass

    def __init__(self, http, client, opts):
        self.http = http
        self.client = client
        self.opts = opts
        
    def do(self):
        raise NotImplementedError()


def load_actions():
    plugs = []
    path = os.path.split(plugins.__file__)[0]
    for fname in os.listdir(path):
        mod, ext = os.path.splitext(fname)
        fname = os.path.join(path, fname)
        if os.path.isfile(fname) and ext == '.py' and not mod.startswith('_'):
            m = importlib.import_module('cli.actions.' + mod)
            for c in dir(m):
                cls = getattr(m, c)
                if not c.startswith('_') and isclass(cls) and issubclass(cls, Action) \
                        and Action != cls:
                    plugs.append(cls)

    return {cls.__name__.lower():cls for cls in plugs}