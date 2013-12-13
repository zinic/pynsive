Using Pynsive
=============


Creating and Using a Plugin Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The plugin context is a nice way of managing what directories you've
plugged into the **sys.meta\_path** variable. Managers may be destroyed
when no longer needed. Destroying a manager removes all directories that
the manager plugged into from the **sys.meta\_path** variable.

::

    import pynsive

    plugin_manager = pynsive.PluginManager()
    plugin_manager.plug_into('/some/path')

    try:
        import myplugins.module.plugin_a as plugin
        print('Imported plugin module: {1}', plugin)
    finally:
        plugin_manager.destroy()


Discovering Python Modules
~~~~~~~~~~~~~~~~~~~~~~~~~~

Pynsive allows you to search a given directory tree for potential module
names to aid in discovery of interesting code. These functions will search
any directories found under the directory specified for python modules and
will recurse as specified by their names.

::

    import pynsive

    # Non-recursive search
    found_modules = pynsive.discover_modules('/some/path')
    print('Discovered {1} modules.', len(found_modules))

    # Recursive search
    found_modules = pynsive.rdiscover_modules('/some/path')
    print('Discovered {1} modules.', len(found_modules))


Dynamically Listing Submodules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note:** The list functions in Pynsive **will not** descend into the
submodules that may exist under the specified module. In order to recursively
search use the rlist functions.

::

    import pynsive
    import test_module

    plugin_manager = pynsive.PluginManager()
    plugin_manager.plug_into('/some/path')

    try:
        found_modules = pynsive.list_modules('ext.plugins')
        print('Discovered {1} modules.', len(found_modules))
    finally:
        plugin_manager.destroy()


Dynamically Finding Classes in a Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note:** The list functions in Pynsive **will not** descend into the
submodules that may exist under the specified module. In order to recursively
search use the rlist functions.

::

    import pynsive
    import test_module

    plugin_manager = pynsive.PluginManager()
    plugin_manager.plug_into('/some/path')

    try:
        def subclasses_only(type_to_test):
            same = type_to_test is not test_module.MyClass
            is_subclass = issubclass(type_to_test, test_module.MyClass)
            return not same and is_subclass

        classes = pynsive.list_classes('ext.plugins', subclasses_only)
        print('Discovered {1} classes.', len(classes))
    finally:
        plugin_manager.destroy()


Dynamically Finding Classes in a Module and its Submodules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note:** The rlist functions in Pynsive **will** descend into the submodules
that may exist under the specified module. In order to perform a non-recursive
listing use the list functions.

::

    import pynsive
    import test_module

    plugin_manager = pynsive.PluginManager()
    plugin_manager.plug_into('/some/path')

    try:
        def subclasses_only(type_to_test):
            same = type_to_test is not test_module.MyClass
            is_subclass = issubclass(type_to_test, test_module.MyClass)
            return not same and is_subclass

        classes = pynsive.rlist_classes('ext.plugins', subclasses_only)
        print('Discovered {1} classes.', len(classes))
    finally:
        plugin_manager.destroy()
