import sys
import unittest

import pynsive


class WhenCreatingThePluginManager(unittest.TestCase):
    def setUp(self):
        self.manager = pynsive.PluginManager()

    def tearDown(self):
        self.manager.destroy()

    def test_correct_meta_path_insertion(self):
        finder_index = sys.meta_path.index(self.manager.finder)
        if sys.version_info >= (3, 1, 0):
            self.assertEqual(0, finder_index)
        else:
            self.assertEqual(len(sys.meta_path) - 1, finder_index)
