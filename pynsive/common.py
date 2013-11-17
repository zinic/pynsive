import importlib


# Constants; because they make the code look nice.
MODULE_PATH_SEP = '.'
MODULE_INIT_FILE = '__init__.py'
NAME_ATTRIBUTE = '__name__'
PATH_ATTRUBITE = '__path__'
PYCACHE_FOLDER = '__pycache__'


def import_module(module_name):
    """
    A nice namespace alias for users.
    """
    return importlib.import_module(module_name)
