import sys

def import_module(name):
    __import__(name)
    return sys.modules[name]

def module_member(name):
    mod, member = name.rsplit('.', 1)
    module = import_module(mod)
    return getattr(module, member)
