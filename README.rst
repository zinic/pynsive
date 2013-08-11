Pynsive
=======

Pronounced, "Pensive"
~~~~~~~~~~~~~~~~~~~~~

This is a simple plugin library that uses the **sys.meta\_path** list
along with custom finder and loader definitions to hook into the Python
import process.

For more information on the import process hooks, please see:

-  `Python 3 Import Process <http://docs.python.org/3/reference/import.html>`_
-  `PEP-302 <http://www.python.org/dev/peps/pep-0302/>`_

Latest Release Notes
~~~~~~~~~~~~~~~~~~~~

This version has the following changes from release version <=0.1.4

-  **discover\_classes** was renamed to **rlist\_classes**
-  **discover\_modules** was renamed to **list\_modules**

Documentation
~~~~~~~~~~~~~

-  `Getting started with Pynsive <http://www.giantflyingsaucer.com/blog/?p=4634>`_
-  `Pynsive at Readthedocs <https://pynsive.readthedocs.org>`_

Examples
~~~~~~~~

Creating a Plugin Context
^^^^^^^^^^^^^^^^^^^^^^^^^

The plugin context is a nice way of managing what directories you've
plugged into the **sys.meta\_path** variable. Managers may be destroyed
when no longer needed. Destroying a manager removes all directories that
the manager plugged into from the **sys.meta\_path** variable.

::

    import pynsive

    plugin_manager = pynsive.PluginManager()
    plugin_manager.plug_into('/some/path')

    try:
    #   Some code goes here
    finally:
        plugin_manager.destroy()

Dynamically Listing Submodules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    import pynsive
    import test_module

    plugin_manager = pynsive.PluginManager()
    plugin_manager.plug_into('/some/path')

    try:
        found_modules = pynsive.list_modules('ext.plugins')
    finally:
        plugin_manager.destroy()

Dynamically Finding Classes in a Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
    finally:
        plugin_manager.destroy()

Dynamically Finding Classes in a Module Tree
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
        # Recursively find classes
        classes = pynsive.rlist_classes('ext.plugins', subclasses_only)
    finally:
        plugin_manager.destroy()

Unit Tests
^^^^^^^^^^

-  `Pynsive Unittest <https://github.com/zinic/pynsive/blob/master/tests/plugin_test.py>`_

That Legal Thing...
~~~~~~~~~~~~~~~~~~~

This software library is released to you under the
`Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_
. See `LICENSE <https://github.com/zinic/pynsive/blob/master/LICENSE>`_ for
more information.

