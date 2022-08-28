import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.Type import Color, Type, Fit, Mission, Brand

class TestTypes(unittest.TestCase):

    def setUp(self) -> None:
        """
        Objects that are initialized in here are created
        when we create the class and run the tests.
        """
        self.color_brown = Color("brown")
        self.color_brown_faded = Color("brown", True)
        self.color_black = Color("black")

        self.fit_slim = Fit.slim
        self.fit_oversized = Fit.oversized

        self.type_hat = Type.hat
        self.type_pants = Type.pants

        self.mission_casual = Mission.casual
        self.mission_formal = Mission.formal

        self.brand_stussy = Brand("Stussy")
        self.brand_stussy_nike = Brand("Stussy", True, ["Nike"])
        self.brand_celine = Brand("Celine")

    def tearDown(self) -> None:
        """
        Objects to be destroyed are put here when the tests are over
        """
        return super().tearDown()

    def test_color(self) -> None:
        self.assertNotEqual(self.color_black, self.color_brown)
        self.assertNotEqual(self.color_brown, self.color_brown_faded)

    def test_type(self) -> None:
        self.assertNotEqual(self.type_hat, self.type_pants)

    def test_fit(self) -> None:
        self.assertNotEqual(self.fit_slim, self.fit_oversized)

    def test_mission(self) -> None:
        self.assertNotEqual(self.mission_casual, self.mission_formal)

    def test_brand(self) -> None:
        self.assertNotEqual(self.brand_stussy, self.brand_stussy_nike)
        self.assertEqual(self.brand_celine.collab, self.brand_stussy.collab)
        self.assertEqual(self.brand_stussy.brand, self.brand_stussy_nike.brand)
        self.assertNotEqual(self.brand_celine.collaborators, self.brand_stussy_nike.collaborators)

# Running the unit tests above
if __name__ == "__main__":
    unittest.main()