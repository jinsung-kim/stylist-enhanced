from __future__ import annotations
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_objects import *
from models.KeyValueStore import KeyValueStore

class TestKeyValuePairs(unittest.TestCase):

    def setUp(self) -> None:
        """
        Objects that are initialized in here are created
        when we create the class and run the tests.
        """
        self.brand_store = KeyValueStore("brand")
        self.type_store = KeyValueStore("type")

    def tearDown(self) -> None:
        """
        Objects to be destroyed are put here when the tests are over
        """
        return super().tearDown()

    def test_store(self):
        self.brand_store.store(brand_stussy, brand_stussy_nike, 2)
        self.brand_store.store(brand_celine, brand_stussy, 0.25)

        self.assertEqual(len(self.brand_store.vals), 2)
        self.assertEqual(self.brand_store.find(brand_stussy, brand_stussy_nike), 2)
        self.assertEqual(self.brand_store.find(brand_stussy, brand_celine), 0.25)

    def test_keys(self):
        self.assertEqual(KeyValueStore._generate_key(type_hat, type_pants), "Category.hat_Category.pants")

    def test_naming(self):
        self.assertEqual(self.brand_store.name, "brand")
        self.assertEqual(self.type_store.name, "type")

# Running the unit tests above
if __name__ == "__main__":
    unittest.main()