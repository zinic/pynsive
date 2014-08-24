import os
import shutil
import tempfile
import unittest
import pynsive


INIT_PY = ""

TEST_CLASSES_PY = """
SUCCESS = True

class PynsiveTestingClass(object):
    pass


class OtherPynsiveTestingClass(PynsiveTestingClass):
    pass
"""


class WhenLoading(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        This crazy setUp method for the following unit tests creates a
        temporary plugin directory and then drops a Python module and related
        testing code into it. The method then spins up a plugin context via
        a pynsive.PluginManager instance.
        """
        cls.directory = tempfile.mkdtemp()

        cls.module_path = os.path.join(cls.directory, 'pynsive_test')
        os.mkdir(cls.module_path)
        with open(os.path.join(cls.module_path, '__init__.py'), 'w') as f:
            f.write(INIT_PY)
        with open(os.path.join(cls.module_path, 'test_classes.py'), 'w') as f:
            f.write(TEST_CLASSES_PY)

        embedded_module = os.path.join(cls.module_path, 'embedded')
        os.mkdir(embedded_module)
        with open(os.path.join(embedded_module, '__init__.py'), 'w') as f:
            f.write('\n')
        with open(os.path.join(embedded_module, 'test.py'), 'w') as f:
            f.write('\n')

        # Adding sub-sub module
        sub_module = os.path.join(embedded_module, 'sub')
        os.mkdir(sub_module)
        with open(os.path.join(sub_module, '__init__.py'), 'w') as f:
            f.write('\n')
        with open(os.path.join(sub_module, 'other.py'), 'w') as f:
            f.write(TEST_CLASSES_PY)

        # Adding an empty (without __init__.py) into the package
        # - Pynsive should ignore this folder
        garbage_folder = os.path.join(cls.module_path, 'garbage')
        os.mkdir(garbage_folder)

        cls.plugin_manager = pynsive.PluginManager()
        cls.plugin_manager.plug_into(cls.directory)

    @classmethod
    def tearDownClass(cls):
        cls.plugin_manager.destroy()
        if cls.directory:
            shutil.rmtree(cls.directory)
            pass

    def test_discovering_modules_in_a_directory(self):
        expected_modules = ['pynsive_test']

        discovered_modules = pynsive.discover_modules(WhenLoading.directory)
        self.assertEqual(expected_modules, discovered_modules)

    def test_discovering_modules_in_a_directory_recursively(self):
        expected_modules = [
            'pynsive_test.embedded',
            'pynsive_test.embedded.sub',
            'pynsive_test.embedded.sub.other',
            'pynsive_test.embedded.test',
            'pynsive_test.test_classes']

        discovered_modules = pynsive.rdiscover_modules(WhenLoading.directory)

        for expected in expected_modules:
            self.assertTrue(expected in discovered_modules)

    def test_plugging_into_directory(self):
        """
        When plugging into a directory using a PluginManager, the manager
        will make the new directory available for search when importing
        modules. These modules must be available for import via the
        import_module function provided by pynsive.
        """
        test_module = pynsive.import_module('pynsive_test.test_classes')
        self.assertTrue(test_module.SUCCESS)

    def test_listing_classes(self):
        classes = pynsive.list_classes('pynsive_test.test_classes')
        self.assertEqual(len(classes), 2)

    def test_listing_classes_with_filter(self):
        test_module = pynsive.import_module('pynsive_test.test_classes')

        def subclasses_only(test_type):
            same = test_type is not test_module.PynsiveTestingClass
            is_subclass = issubclass(
                test_type, test_module.PynsiveTestingClass)
            return not same and is_subclass

        classes = pynsive.list_classes('pynsive_test.test_classes',
                                       subclasses_only)
        self.assertEqual(len(classes), 1)

    def test_importing_missing_module(self):
        with self.assertRaises(ImportError):
            pynsive.list_modules('this.is.totally.fake.and.a.bad.name')

    def test_crawling_plugged_in_modules(self):
        found_modules = pynsive.list_modules('pynsive_test')
        self.assertTrue('pynsive_test.test_classes' in found_modules)

    def test_crawling_modules(self):
        found_modules = pynsive.list_modules('pynsive_test')
        self.assertEqual(1, len(found_modules))
        self.assertTrue('pynsive_test.test_classes' in found_modules)

    def test_crawling_modules_recursively(self):
        found_modules = pynsive.rlist_modules('pynsive_test')
        self.assertEqual(5, len(found_modules))
        self.assertTrue('pynsive_test.test_classes' in found_modules)
        self.assertTrue('pynsive_test.embedded' in found_modules)
        self.assertTrue('pynsive_test.embedded.test' in found_modules)

    def test_discovering_classes(self):
        classes = pynsive.list_classes('pynsive_test.test_classes')
        self.assertEqual(2, len(classes))

    def test_recursively_discovering_classes(self):
        classes = pynsive.rlist_classes('pynsive_test')
        self.assertEqual(4, len(classes))

    def test_recursively_listing_classes_with_filter(self):
        test_module = pynsive.import_module('pynsive_test.test_classes')

        def subclasses_only(test_type):
            same = test_type is not test_module.PynsiveTestingClass
            is_subclass = issubclass(
                test_type, test_module.PynsiveTestingClass)
            print('test class - {}'.format(test_type))
            print(same)
            print(is_subclass)
            return not same and is_subclass

        classes = pynsive.rlist_classes('pynsive_test', subclasses_only)
        self.assertEqual(len(classes), 1)
