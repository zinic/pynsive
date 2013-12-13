[![Build Status](http://jenkins.projectmeniscus.org/job/Pynsive/badge/icon)](http://jenkins.projectmeniscus.org/job/Pynsive/)

# Pynsive
#### Pronounced, "Pensive"

This is a simple plugin library that uses the **sys.meta_path** list along
with custom finder and loader definitions to hook into the Python import
process.

For more information on the import process hooks, please see:

* [Python 3 Import Process](http://docs.python.org/3/reference/import.html)
* [PEP-302](http://www.python.org/dev/peps/pep-0302/)

### Documentation

* [Pynsive at Readthedocs](https://pynsive.readthedocs.org)
* [Pynsive at Pypi](https://pypi.python.org/pypi/pynsive)
* [Getting started with Pynsive by Chad Lung](http://www.giantflyingsaucer.com/blog/?p=4634)
* [Pynsive: A Simple Plugin Library for Python – A Second Look by Chad Lung](http://www.giantflyingsaucer.com/blog/?p=4695)


### Examples

#### Creating and Using a Plugin Context
<a href="#creating-a-plugin-context" />

The plugin context is a nice way of managing what directories you've plugged
into the **sys.meta_path** variable. Managers may be destroyed when no
longer needed. Destroying a manager removes all directories that the manager
plugged into from the **sys.meta_path** variable.

```python
import pynsive

plugin_manager = pynsive.PluginManager()
plugin_manager.plug_into('/some/path')

try:
    import myplugins.module.plugin_a as plugin
    print('Imported plugin module: {1}', plugin)
finally:
    plugin_manager.destroy()
```

#### Discovering Python Modules
<a href="#discovering-python-modules" />

Pynsive allows you to search a given directory tree for potential module
names to aid in discovery of interesting code. These functions will search
any directories found under the directory specified for python modules and
will recurse as specified by their names.

```python
import pynsive

# Non-recursive search
found_modules = pynsive.discover_modules('/some/path')
print('Discovered {1} modules.', len(found_modules))

# Recursive search
found_modules = pynsive.rdiscover_modules('/some/path')
print('Discovered {1} modules.', len(found_modules))
```

#### Dynamically Listing Submodules
<a href="#dynamically-listing-submodules" />

**Note:** The list functions in Pynsive **will not** descend into the
submodules that may exist under the specified module. In order to recursively
search use the rlist functions.

```python
import pynsive
import test_module

plugin_manager = pynsive.PluginManager()
plugin_manager.plug_into('/some/path')

try:
    found_modules = pynsive.list_modules('ext.plugins')
    print('Discovered {1} modules.', len(found_modules))
finally:
    plugin_manager.destroy()
```

#### Dynamically Finding Classes in a Module
<a href="#dynamically-finding-classes-in-a-module" />

**Note:** The list functions in Pynsive **will not** descend into the
submodules that may exist under the specified module. In order to recursively
search use the rlist functions.

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
    print('Discovered {1} classes.', len(classes))
finally:
    plugin_manager.destroy()
```

#### Dynamically Finding Classes in a Module and its Submodules
<a href="#dynamically-finding-classes-in-a-module-tree" />

**Note:** The rlist functions in Pynsive **will** descend into the submodules
that may exist under the specified module. In order to perform a non-recursive
listing use the list functions.

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
    print('Discovered {1} classes.', len(classes))
finally:
    plugin_manager.destroy()
```


##That Legal Thing...

This software library is released to you under the [MIT License](http://opensource.org/licenses/MIT). See [LICENSE](https://github.com/zinic/pynsive/blob/master/LICENSE) for more information.
