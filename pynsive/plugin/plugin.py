import sys
import os.path
import importlib

from .loader import SecureLoader


# Constants; because they make the code look nice.
_MODULE_PATH_SEP = '.'
_NAME = '__name__'
_PATH = '__path__'


class PluginError(ImportError):

    def __init__(self, msg):
        self.msg = msg


class PluginFinder(object):

    def __init__(self, paths=None):
        if paths is None:
            paths = list()
        self.paths = paths

    def add_path(self, new_path):
        if new_path not in self.paths:
            self.paths.append(new_path)

    def find_module(self, fullname, path=None):
        module_path = os.path.join(*fullname.split(_MODULE_PATH_SEP))

        for plugin_path in self.paths:
            target_path = os.path.join(plugin_path, module_path)
            is_pkg = False

            # If the target references a directory, try to load it as
            # a module by referencing the __init__.py file, otherwise
            # append .py and attempt to resolve it.
            if os.path.isdir(target):
                target_file = os.path.join(target, '__init__.py')
                is_pkg = True
            else:
                target_file = '{}.py'.format(target)

            if os.path.exists(target):
                return SecureLoader(fullname, target_path, target_file, is_pkg)

        return None


class PluginManager(object):

    def __init__(self):
        self.finder = PluginFinder()
        sys.meta_path.append(self.finder)

    def __del__(self):
        sys.meta_path.remove(self.finder)

    def plug_into(self, *paths):
        """
        Adds all arguments passed as plugin directories to search when loading
        modules.
        """
        [self.finder.add_path(path) for path in args]

    def import_module(module_name):
        """
        This function ensures that the directory hooks have been placed in the
        sys.meta_path list before passing the module name being required to
        the importlib call of the same name.
        """
        return importlib.import_module(module_name)



