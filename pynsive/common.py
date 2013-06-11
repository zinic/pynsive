import importlib


# Constants; because they make the code look nice.
MODULE_PATH_SEP = '.'
NAME = '__name__'
PATH = '__path__'


def import_module(module_name):
    """
    A nice namespace alias for users.
    """
    return importlib.import_module(module_name)
