import imp
import sys
import os

from ..common import *


class LoaderError(ImportError):
    """
    This error is thrown when the module loader encounters an exception or
    an unrecoverable state while attempting to load a dynamically located
    module.
    """
    def __init__(self, msg):
        """
        Creates a loader error.

        :param msg: the loader error message to relay upwards
        """
        self.msg = msg


class ModuleLoader(object):
    """
    As per PEP302, this module loader provides all of the necessary context
    for loading a python file and executing its contents.
    """
    def __init__(self, module_path, module_name, load_target, is_pkg):
        """
        Creates a new module loader.

        :param module_path: the path where the module resides
        :param module_name: the full name of the module to load
        :param load_target: the absolute path of the module file to load
        :param is_pkg: true if this module is a package, false otherwise
        """
        self.module_path = module_path
        self.module_name = module_name
        self.load_target = load_target
        self.is_pkg = is_pkg

    def load_module_py_path(self, module_name, path):
        file_ext = os.path.splitext(path)[1]
        module = None
        if file_ext.lower() == '.py':
            module = imp.load_source(module_name, path)
        elif file_ext.lower() == '.pyc':
            module = imp.load_compiled(module_name, path)

        return module

    def load_module(self, module_name):
        """
        Loads a module's code and sets the module's expected hidden
        variables. For more information on these variables and what they
        are for, please see PEP302.

        :param module_name: the full name of the module to load
        """
        if module_name != self.module_name:
            raise LoaderError(
                'Requesting a module that the loader is unaware of.')

        if module_name in sys.modules:
            return sys.modules[module_name]

        module = self.load_module_py_path(module_name, self.load_target)
        if self.is_pkg:
            module.__path__ = [self.module_path]
            module.__package__ = module_name
        else:
            module.__package__ = module_name.rpartition('.')[0]

        sys.modules[module_name] = module
        return module


class ModuleFinder(object):
    """
    As per PEP302, this module loader provides all of the necessary context
    for dynamically locating python modules based. This finder searches
    directories based on paths added to its internal list of available
    search directories.
    """
    def __init__(self, paths=None):
        """
        Creates a module finder.

        :param paths: the paths to include in the search list by default
        """
        self.paths = paths if paths else list()

    def add_path(self, path):
        """
        Adds a path to search through when attempting to look up a module.

        :param path: the path the add to the list of searchable paths
        """
        if path not in self.paths:
            self.paths.append(path)

    def find_module(self, module_name, path=None):
        """
        Searches the paths for the required module.

        :param module_name: the full name of the module to find
        :param path: set to None when the module in being searched for is a
                     top-level module - otherwise this is set to
                     package.__path__ for submodules and subpackages (unused)
        """
        module_path = os.path.join(*module_name.split(MODULE_PATH_SEP))

        for search_root in self.paths:
            target_path = os.path.join(search_root, module_path)
            is_pkg = False

            # If the target references a directory, try to load it as
            # a module by referencing the __init__.py file, otherwise
            # append .py and attempt to resolve it.
            if os.path.isdir(target_path):
                target_file = os.path.join(target_path, '__init__.py')
                is_pkg = True
            else:
                target_file = '{}.py'.format(target_path)

            if os.path.exists(target_file):
                return ModuleLoader(
                    target_path, module_name, target_file, is_pkg)
        return None
