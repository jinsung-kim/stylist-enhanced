from __future__ import annotations
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.Models import Color, Category, Fit, Mission, Brand, ClothingItem

color_brown = Color("brown")
color_brown_faded = Color("brown", True)
color_black = Color("black")

fit_slim = Fit.slim
fit_oversized = Fit.oversized

type_hat = Category.hat
type_pants = Category.pants

mission_casual = Mission.casual
mission_formal = Mission.formal

brand_stussy = Brand("Stussy")
brand_stussy_nike = Brand("Stussy", True, ["Nike"])
brand_celine = Brand("Celine")

clothing_item1: ClothingItem = ClothingItem( "Stussy T shirt", brand_stussy, [color_black], \
                                            fit_oversized, type_hat, [mission_casual])

clothing_item2: ClothingItem = ClothingItem("Stussy Nike Beanie", brand_stussy_nike, [color_black], \
                                            fit_slim, type_hat, [mission_casual])