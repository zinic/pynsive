import os
import shutil
import tempfile
import unittest
import pynsive


class WhenLoading(unittest.TestCase):

    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.module_path = os.path.join(self.directory, 'pynsive_test')
        os.mkdir(self.module_path)
        with open(os.path.join(self.module_path, '__init__.py'), 'w') as f:
            f.write(
"""
from .test_classes import *

""")
        with open(os.path.join(self.module_path, 'test_classes.py'), 'w') as f:
            f.write(
"""
SUCCESS = True

class PynsiveTestingClass(object):
    pass


class OtherPynsiveTestingClass(PynsiveTestingClass):
    pass

""")
        self.plugin_manager = pynsive.PluginManager()
        self.plugin_manager.plug_into(self.directory)


    def tearDown(self):
        if self.directory:
            shutil.rmtree(self.directory)

    def test_plugging_into_directory(self):
        test_module = pynsive.import_module('pynsive_test.test_classes')
        self.assertTrue(test_module.SUCCESS)

    def test_listing_classes(self):
        classes = pynsive.list_classes('pynsive_test')
        self.assertEqual(len(classes), 2)

    def test_listing_classes_with_filter(self):
        test_module = pynsive.import_module('pynsive_test.test_classes')
        def subclasses_only(test_type):
            same = test_type is not test_module.PynsiveTestingClass
            is_subclass = issubclass(test_type, test_module.PynsiveTestingClass)
            return not same and is_subclass
        classes = pynsive.list_classes('pynsive_test', type_filter)
        self.assertEqual(len(classes), 1)

