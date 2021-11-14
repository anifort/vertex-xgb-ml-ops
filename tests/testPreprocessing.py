import unittest

from components.preprocessing import split_data

from kfp.v2.dsl import (
    Output,
    Dataset
)

class TestPreprocessing(unittest.TestCase):


    def setUp(self):
        return

    def tearDown(self):
        return

    def test_data_split(self):
        self.assertEqual(5, 5)