"""
This is a simple plugin layer that uses the sys.meta_path list along
with custom finder and loader definitions to hook into the Python
import process. For more information, please see:
http://www.python.org/dev/peps/pep-0302/
"""
import imp
import sys
import os.path
import importlib
import inspect


# Constants; because they make the code look nice.
_MODULE_PATH_SEP = '.'
_NAME = '__name__'
_PATH = '__path__'


def is_python_file(filename):
    return filename.endswith('.py') and os.path.isfile(filename)


class TypeFilter(object):

    def allow(self):
        raise NotImplementedError


class PluginError(ImportError):

    def __init__(self, msg):
        self.msg = msg


class ModuleInspector(object):

    def __init__(self, plugin_finder):
        self.plugin_finder = plugin_finder

    def find_classes_in_module(self, entry_name, type_filter=None):
        found = list()
        for mname in self.list_modules(entry_name):
            module = import_module(mname)
            [found.append(mod) for mod in self.list_classes_in_module(
                module, type_filter)]
        return found

    def list_classes_in_module(self, module, type_filter):
        found = list()

        for name, module_obj in inspect.getmembers(module):
            if inspect.isclass(module_obj):
                append = not type_filter or type_filter(type(module_obj))
                if append:
                    found.append(module_obj)

        return found

    def list_modules(self, mname):
        # Path to the module that we want to explore
        path = os.path.join(*mname.split(_MODULE_PATH_SEP))

        # Gather the modules from the plugin paths first - these take priority
        modules = self.find_modules(mname, path, self.plugin_finder.paths)

        if len(modules) == 0:
            # Check for the module in the system paths if no matches were found
            modules = self.find_modules(mname, path, sys.path)
        return modules

    def find_modules(self, mname, mpath, scan_paths):
        modules = list()

        # Scan all of the places specified by scan_paths
        for path in scan_paths:
            target = os.path.join(path, mpath)
            if os.path.isdir(target):
                for child_mod in self._list_dir_moduels(target):
                    child_fullname = '{}{}{}'.format(
                        mname, _MODULE_PATH_SEP, child_mod)
                    modules.append(child_fullname)
            elif os.path.isfile(target):
                modules.append(mname)
        return modules

    def _list_dir_moduels(self, directory):
        module_files = list()
        for name in os.listdir(directory):
            if is_python_file(os.path.join(directory, name)):
                module_files.append(name[:len(name)-3])
        return module_files


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
            target = os.path.join(plugin_path, module_path)
            is_pkg = False

            # If the target references a directory, try to load it as
            # a module by referencing the __init__.py file, otherwise
            # append .py and attempt to resolve it.
            if os.path.isdir(target):
                target = os.path.join(target, '__init__.py')
                is_pkg = True
            else:
                target += '.py'

            if os.path.exists(target):
                return SecureLoader(fullname, target, is_pkg)

        return None


class SecureLoader(object):

    def __init__(self, module_name, target, is_pkg):
        self.module_name = module_name
        self.load_target = target
        self.is_pkg = is_pkg

    def _read_code(self):
        fin = open(self.load_target, 'r')
        code = fin.read()
        fin.close()
        return code

    def load_module(self, fullname):
        if fullname != self.module_name:
            raise PluginError('Requesting a module that the loader is '
                              'unaware of.')

        if fullname in sys.modules:
            return sys.modules[fullname]

        code = self._read_code()
        module = imp.new_module(fullname)
        module.__file__ = self.load_target
        module.__loader__ = self

        if self.is_pkg:
            module.__path__ = []
            module.__package__ = fullname
        else:
            module.__package__ = fullname.rpartition('.')[0]

        exec(code, module.__dict__)
        sys.modules[fullname] = module
        return module


# Plugin finder singleton
_PLUGIN_FINDER = PluginFinder()
_MOD_INSPECTOR = ModuleInspector(_PLUGIN_FINDER)

"""
Injects a custom finder object into the sys.meta_path list in order to
allow for the loading of additional modules that may not be in the path
given to the interpreter at boot.
"""
if _PLUGIN_FINDER not in sys.meta_path:
    sys.meta_path.append(_PLUGIN_FINDER)


def import_module(module_name):
    """
    This function ensures that the directory hooks have been placed in the
    sys.meta_path list before passing the module name being required to
    the importlib call of the same name.
    """
    return importlib.import_module(module_name)


def module_inspector():
    return _MOD_INSPECTOR


def plug_into(*args):
    """
    Adds all arguments passed as plugin directories to search when loading
    modules.
    """
    for path in args:
        _PLUGIN_FINDER.add_path(path)
