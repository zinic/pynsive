import sys
import os.path
import inspect

from .common import *


def list_classes(mname, type_filter=None):
    found = list()
    module = import_module(mname)
    if inspect.ismodule(module):
        [found.append(mod) for mod in _list_classes(module, type_filter)]
    return found


def _list_classes(module, type_filter):
    found = list()

    for name, module_obj in inspect.getmembers(module):
        if inspect.isclass(module_obj):
            append = not type_filter or type_filter(module_obj)
            if append:
                found.append(module_obj)
    return found
