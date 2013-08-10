# Pynsive
#### Pronounced, "Pensive"

This is a simple plugin library that uses the **sys.meta_path** list along with custom finder and loader definitions to hook into the Python import process.

For more information on the import process hooks, please see:

* [Python 3 Import Process](http://docs.python.org/3/reference/import.html)
* [PEP-302](http://www.python.org/dev/peps/pep-0302/)


### Latest Release Notes (0.1.5)

Upgrading to this version has the following changes from the previous
release (0.1.4).

* **discover_classes** was renamed to **rlist_classes**
* **discover_modules** was renamed to **list_modules**


### Usage

#### Creating a Plugin Context

The plugin context is a nice way of managing what directories you've plugged
into the **sys.meta_path** variable. Managers may be destroyed when no longer
needed. Destroying a manager removes all directories that the manager
plugged into from the **sys.meta_path** variable.

```python
import pynsive

plugin_manager = pynsive.PluginManager()
plugin_manager.plug_into('/some/path')

try:
#   Some code goes here
finally:
    plugin_manager.destroy()
```

#### Dynamically Listing Modules under a Module

```python
import pynsive
import test_module

plugin_manager = pynsive.PluginManager()
plugin_manager.plug_into('/some/path')

try:
    found_modules = pynsive.list_modules('ext.plugins')
finally:
    plugin_manager.destroy()
```

#### Dynamically Finding Classes in a Single Module by Subclass

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

    classes = pynsive.rlist_classes('ext.plugins', subclasses_only)
finally:
    plugin_manager.destroy()
```

## Unit Test Examples
* [Pynsive Unittest](https://github.com/zinic/pynsive/blob/master/tests/plugin_test.py)

## Beginner's Tutorial
* [Getting started with Pynsive](http://www.giantflyingsaucer.com/blog/?p=4634)

##That Legal Thing...

This software library is released to you under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html). See [LICENSE](https://github.com/zinic/pynsive/blob/master/LICENSE) for more information.
