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
        self.msg = msg


class ModuleLoader(object):
    """
    As per PEP302, this module loader provides all of the necessarry context
    for loading a python file and executing its contents.
    """

    def __init__(self, module_path, module_name, load_target, is_pkg):
        self.module_path = module_path
        self.module_name = module_name
        self.load_target = load_target
        self.is_pkg = is_pkg

    def _read_code(self):
        """
        Simple abstraction to make reading a module file easy.
        """
        fin = open(self.load_target, 'r')
        code = fin.read()
        fin.close()
        return code

    def load_module(self, fullname):
        """
        Loads a module's code and sets the module's expected hidden
        variables. For more information on these variables and what they
        are for, please see PEP302.
        """
        if fullname != self.module_name:
            raise LoaderError(
                'Requesting a module that the loader is unaware of.')

        if fullname in sys.modules:
            return sys.modules[fullname]

        code = self._read_code()
        module = imp.new_module(fullname)
        module.__file__ = self.load_target
        module.__loader__ = self

        if self.is_pkg:
            module.__path__ = [self.module_path]
            module.__package__ = fullname
        else:
            module.__package__ = fullname.rpartition('.')[0]

        sys.modules[fullname] = module
        exec(code, module.__dict__)
        return module


class ModuleFinder(object):
    """
    As per PEP302, this module loader provides all of the necessarry context
    for dynamically locating python modules based. This finder searches
    directories based on paths added to its internal list of available
    search directories.
    """

    def __init__(self, paths=None):
        self.paths = paths if paths else list()

    def add_path(self, new_path):
        """
        Adds a path to search through when attempting to look up a module.
        """
        if new_path not in self.paths:
            self.paths.append(new_path)

    def find_module(self, fullname, path=None):
        """
        Searches the paths for the required module.
        """
        module_path = os.path.join(*fullname.split(MODULE_PATH_SEP))

        for plugin_path in self.paths:
            target_path = os.path.join(plugin_path, module_path)
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
                return ModuleLoader(target_path, fullname, target_file, is_pkg)

        return None
