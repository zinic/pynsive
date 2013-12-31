import sys
import os.path
import inspect

from .common import *


def _list_classes(module, cls_filter):
    found = list()
    for name, module_obj in inspect.getmembers(module):
        if inspect.isclass(module_obj):
            append = not cls_filter or cls_filter(module_obj)
            if append:
                found.append(module_obj)
    return found


def _scan_paths_for(mname, paths):
    mpath_part = mname.replace(MODULE_PATH_SEP, os.sep)
    for mpath in paths:
        scan_target = os.path.join(mpath, mpath_part)
        is_dir = os.path.isdir(scan_target)
        is_file = os.path.isfile('{}.py'.format(scan_target))
        if is_dir or is_file:
            return mpath


def _should_use_module_path(module):
    """
    Checks to make sure that the passed module has the correct hidden
    variables set.
    """
    return hasattr(module, PATH_ATTRUBITE) and len(module.__path__) > 0


def _search_for_modules(directory, recursive=False, prefix=None):
    found = list()

    # Scan only if there's an __init__.py file
    if os.path.isfile(os.path.join(directory, MODULE_INIT_FILE)):
        for entry in os.listdir(directory):
            # Skip the init file
            if entry == MODULE_INIT_FILE:
                continue

            # Skip the pycache folder
            if entry == PYCACHE_FOLDER:
                continue

            if entry.endswith('.py'):
                module = entry[:len(entry)-3]

                if prefix:
                    found.append(MODULE_PATH_SEP.join((prefix, module)))
                else:
                    found.append(module)
            elif recursive:
                next_dir = os.path.join(directory, entry)

                if os.path.isdir(next_dir):
                    if prefix:
                        next_mod = MODULE_PATH_SEP.join((prefix, entry))
                    else:
                        next_mod = entry

                    # Make sure it's actually a module
                    next_mod_init = os.path.join(next_dir, MODULE_INIT_FILE)
                    if os.path.isfile(next_mod_init):
                        found.append(next_mod)
                        found.extend(_search_for_modules(next_dir, True,
                                                         next_mod))
    return found


def _discover_modules(directory, recursive=False):
    found = list()

    if os.path.isdir(directory):
        for entry in os.listdir(directory):
            next_dir = os.path.join(directory, entry)

            # Scan only if there's an __init__.py file
            if os.path.isfile(os.path.join(next_dir, MODULE_INIT_FILE)):
                modules = _search_for_modules(next_dir, recursive, entry)
                found.extend(modules)

    return found


def discover_modules(directory):
    """
    Attempts to list all of the modules and submodules found within a given
    directory tree. This function searches the top-level of the directory
    tree for potential python modules and returns a list of candidate names.

    **Note:** This function returns a list of strings representing
    discovered module names, not the actual, loaded modules.

    :param directory: the directory to search for modules.
    """
    found = list()

    if os.path.isdir(directory):
        for entry in os.listdir(directory):
            next_dir = os.path.join(directory, entry)

            # Scan only if there's an __init__.py file
            if os.path.isfile(os.path.join(next_dir, MODULE_INIT_FILE)):
                found.append(entry)

    return found


def rdiscover_modules(directory):
    """
    Attempts to list all of the modules and submodules found within a given
    directory tree. This function recursively searches the directory tree
    for potential python modules and returns a list of candidate names.

    **Note:** This function returns a list of strings representing
    discovered module names, not the actual, loaded modules.

    :param directory: the directory to search for modules.
    """
    found = list()

    if os.path.isdir(directory):
        for entry in os.listdir(directory):
            next_dir = os.path.join(directory, entry)

            # Scan only if there's an __init__.py file
            if os.path.isfile(os.path.join(next_dir, MODULE_INIT_FILE)):
                modules = _search_for_modules(next_dir, True, entry)
                found.extend(modules)

    return found


def list_modules(mname):
    """
    Attempts to list all of the submodules under a module. This function
    works for modules located in the default path as well as extended paths
    via the sys.meta_path hooks.

    This function carries the expectation that the hidden module variable
    '__path__' has been set correctly.

    :param mname: the module name to descend into
    """
    module = import_module(mname)
    if not module:
        raise ImportError('Unable to load module {}'.format(mname))

    found = list()
    if _should_use_module_path(module):
        mpath = module.__path__[0]
    else:
        mpaths = sys.path
        mpath = _scan_paths_for(mname, mpaths)

    if mpath:
        for pmname in _search_for_modules(mpath):
            found_mod = MODULE_PATH_SEP.join((mname, pmname))
            found.append(found_mod)
    return found


def rlist_modules(mname):
    """
    Attempts to the submodules under a module recursively. This function
    works for modules located in the default path as well as extended paths
    via the sys.meta_path hooks.

    This function carries the expectation that the hidden module variable
    '__path__' has been set correctly.

    :param mname: the module name to descend into
    """
    module = import_module(mname)
    if not module:
        raise ImportError('Unable to load module {}'.format(mname))

    found = list()
    if _should_use_module_path(module):
        mpath = module.__path__[0]
    else:
        mpaths = sys.path
        mpath = _scan_paths_for(mname, mpaths)

    if mpath:
        for pmname in _search_for_modules(mpath, recursive=True):
            found_mod = MODULE_PATH_SEP.join((mname, pmname))
            found.append(found_mod)
    return found


def list_classes(mname, cls_filter=None):
    """
    Attempts to list all of the classes within a specified module. This
    function works for modules located in the default path as well as
    extended paths via the sys.meta_path hooks.

    If a class filter is set, it will be called with each class as its
    parameter. This filter's return value must be interpretable as a
    boolean. Results that evaluate as True will include the type in the
    list of returned classes. Results that evaluate as False will exclude
    the type in the list of returned classes.

    :param mname: of the module to descend into
    :param cls_filter: a function to call to determine what classes should be
                included.
    """
    found = list()
    module = import_module(mname)
    if inspect.ismodule(module):
        [found.append(mod) for mod in _list_classes(module, cls_filter)]
    return found


def rlist_classes(module, cls_filter=None):
    """
    Attempts to list all of the classes within a given module namespace.
    This method, unlike list_classes, will recurse into discovered
    submodules.

    If a type filter is set, it will be called with each class as its
    parameter. This filter's return value must be interpretable as a
    boolean. Results that evaluate as True will include the type in the
    list of returned classes. Results that evaluate as False will exclude
    the type in the list of returned classes.

    :param mname: of the module to descend into
    :param cls_filter: a function to call to determine what classes should be
                included.
    """
    found = list()
    mnames = rlist_modules(module)
    for mname in mnames:
        [found.append(c) for c in list_classes(mname, cls_filter)]
    return found
