import sys

from .loader import ModuleFinder


class PluginManager(object):
    """
    The PluginManager class is a nice wrapper for tapping into sys.meta_path
    with pynsive. It also provides a hook for removing itself from
    sys.meta_path.
    """
    def __init__(self):
        self.finder = ModuleFinder()
        sys.meta_path.append(self.finder)

    def destroy(self):
        """
        Removes the meta_path hook associated with this manager.
        """
        sys.meta_path.remove(self.finder)

    def plug_into(self, *paths):
        """
        Adds all arguments passed as plugin directories to search when loading
        modules.
        """
        [self.finder.add_path(path) for path in paths]
