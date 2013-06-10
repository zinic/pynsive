import imp
import sys

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
            raise PluginError(
                'Requesting a module that the loader is unaware of.')

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

