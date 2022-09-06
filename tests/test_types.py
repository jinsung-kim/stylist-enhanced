from __future__ import annotations
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_objects import *

class TestTypes(unittest.TestCase):

    def tearDown(self) -> None:
        """
        Objects to be destroyed are put here when the tests are over
        """
        return super().tearDown()

    def test_color(self) -> None:
        self.assertNotEqual(color_black, color_brown)
        self.assertNotEqual(color_brown, color_brown_faded)

    def test_type(self) -> None:
        self.assertNotEqual(type_hat, type_pants)

    def test_fit(self) -> None:
        self.assertNotEqual(fit_slim, fit_oversized)

    def test_mission(self) -> None:
        self.assertNotEqual(mission_casual, mission_formal)

    def test_brand(self) -> None:
        self.assertNotEqual(brand_stussy, brand_stussy_nike)
        self.assertEqual(brand_celine.collab, brand_stussy.collab)
        self.assertEqual(brand_stussy.brand, brand_stussy_nike.brand)
        self.assertNotEqual(brand_celine.collaborators, brand_stussy_nike.collaborators)

    def test_clothing_item(self) -> None:
        self.assertNotEqual(clothing_item1.item_name, clothing_item2.item_name)
        self.assertEqual(clothing_item1.category, clothing_item2.category)
        self.assertEqual(clothing_item1.trip_mission, clothing_item2.trip_mission)
        self.assertEqual(clothing_item1.primary, clothing_item2.primary)
        self.assertNotEqual(clothing_item1.size, clothing_item2.size)

# Running the unit tests above
if __name__ == "__main__":
    unittest.main()