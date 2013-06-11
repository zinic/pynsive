import sys
import os.path
import inspect

from .common import *


def _list_classes(module, type_filter):
    found = list()

    for name, module_obj in inspect.getmembers(module):
        if inspect.isclass(module_obj):
            append = not type_filter or type_filter(module_obj)
            if append:
                found.append(module_obj)
    return found


def _should_use_module(module):
    return hasattr(module, PATH_ATTRUBITE) and len(module.__path__) > 0


def _scan_paths_for(mname, paths):
    mpath_part = mname.replace(MODULE_PATH_SEP, os.sep)
    for path in paths:
        scan_target = os.path.join(path, mpath_part)
        is_dir = os.path.isdir(scan_target)
        is_file = os.path.isfile('{}.py'.format(scan_target))
        if is_dir or is_file:
            return mpath


def _scan_dir(directory):
    found = list()
    module_py = os.path.join(directory, MODULE_INIT_FILE)
    if os.path.isfile(module_py):
        # Scan only if there's an __init__.py file
        for dir_entry in os.listdir(directory):
            if dir_entry != MODULE_INIT_FILE and dir_entry.endswith('.py'):
                found.append(dir_entry.rstrip('.py'))
    return found


def list_classes(mname, type_filter=None):
    found = list()
    module = import_module(mname)
    if inspect.ismodule(module):
        [found.append(mod) for mod in _list_classes(module, type_filter)]
    return found


def discover_modules(mname):
    found = list()
    module = import_module(mname)

    if module and _should_use_module(module):
        mpath = module.__path__[0]
    else:
        mpaths = sys.path
        mpath = _scan_paths_for(mname, mpaths)

    if mpath:
        for pmname in _scan_dir(mpath):
            found_mod = '{}{}{}'.format(mname, MODULE_PATH_SEP, pmname)
            found.append(found_mod)
    return found


def discover_classes(module, type_filter=None):
    classes = list()
    mnames = discover_modules(module)
    for mname in mnames:
        [classes.append(c) for c in list_classes(mname, type_filter)]
    return classes
