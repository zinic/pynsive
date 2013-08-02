# Pynsive
#### Pronounced, "Pensive"

This is a simple plugin library that uses the sys.meta_path list along with custom finder and loader definitions to hook into the Python import process.

For more information on the import process hooks, please see:

* [Python 3 Import Process](http://docs.python.org/3/reference/import.html)
* [PEP-302](http://www.python.org/dev/peps/pep-0302/)

## Usage

#### Creating a Plugin Context

The plugin context is a nice way of managing what directories you've plugged
into the sys.meta_path variable. Managers may be destroyed when no longer
needed. Destroying a manager removes all directories that the manager
plugged into from the sys.meta_path variable.

```python
import pynsive

plugin_manager = pynsive.PluginManager()
plugin_manager.plug_into('/some/path')

try:
#   Some code goes here
finally:
    plugin_manager.destroy()
```

#### Dynamically Finding Classes in a Single Module by Subtype

```python
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
```

#### Dynamically Finding All Classes in a Module and its Submodules by Subtype

```python
import pynsive
import test_module

plugin_manager = pynsive.PluginManager()
plugin_manager.plug_into('/some/path')

try:
    def subclasses_only(type_to_test):
        same = type_to_test is not test_module.MyClass
        is_subclass = issubclass(type_to_test, test_module.MyClass)
        return not same and is_subclass

    classes = pynsive.discover_classes('ext.plugins', subclasses_only)
finally:
    plugin_manager.destroy()
```

## Unit Test Examples
* [Pynsive Unittest](https://github.com/zinic/pynsive/blob/master/pynsive/tests/plugin_test.py)

##That Legal Thing...

This software library is released to you under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html). See [LICENSE](https://github.com/zinic/pynsive/blob/master/LICENSE) for more information.
