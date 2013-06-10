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
    is_python_filename = len(filename) > 3 and filename.endswith('.py')
    return is_python_filename and os.path.isfile(filename)


class ModuleInspector(object):

    def __init__(self):
        pass

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
        modules = None

        if self.plugin_finder:
            # Gather the modules from the plugin paths first - these take priority
            modules = self.find_modules(mname, path, self.plugin_finder.paths)

        if modules == None or len(modules) == 0:
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
        for fname in os.listdir(directory):
            if is_python_file(os.path.join(directory, fname)):
                # Trim '.py' from the file name
                module_name = fname[:len(fname)-3]
                module_files.append()
        return module_files

