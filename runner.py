from __future__ import annotations
from multiprocessing import parent_process
from posixpath import split
import sys
import os
from xml.dom.expatbuilder import parseString
# import requests
# from decouple import config

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.KeyValueStore import KeyValueStore
from models.Models import *

class Database:
    
    def __init__(self) -> None:
        # Each category organized
        self.items: dict[str, list[ClothingItem]] = {}
        self.curr = ""

    def _generate_brand(self, text: str) -> Brand:
        pass

    def _generate_colors(self, text: str) -> list[Color]:
        split_str: list[str] = text.split("/")
        colors: list[Color] = []

        for color in split_str:
            if "-" in color:
                colors.append(Color(color.split("-")[0], True))
            else:
                colors.append(Color(color))

        return colors

    def _current_category(self) -> Category:
        if self.curr == "HATS":
            return Category.hat
        elif self.curr == "OUTERWEAR":
            return Category.outerwear
        elif self.curr == "TOPS":
            return Category.top
        elif self.curr == "BOTTOMS":
            return Category.pants
        elif self.curr == "SHOES":
            return Category.shoes
        else:
            return Category.undefined

    def _categorize_sizing(self, text: str) -> Fit:
        if text == "Slim":
            return Fit.slim
        elif text == "Regular":
            return Fit.regular
        elif text == "Oversized":
            return Fit.oversized
        else:
            return Fit.undefined

    def load_clothing_from_txt(self, filename: str = "rotation.txt") -> bool:
        txt_file = open(filename, "r")

        lines = txt_file.readlines()

        target = ["HATS", "OUTERWEAR", "TOPS", "BOTTOMS", "SHOES"]
        adding_clothing = True

        # Add each item in its intended category
        for line in lines:
            line = line.strip("\n")
            if line in target:
                self.curr = line
                self.items[self.curr] = []
                adding_clothing = True
            elif len(line) == 0:
                self.curr = ""
                adding_clothing = False
            elif len(line) > 0 and adding_clothing:
                attributes = line.split(",")
                name: str = attributes[0].strip()
                brand: Brand = self._generate_brand(attributes[1].strip())
                colors: list[Color] = self._generate_colors(attributes[2].strip())
                sizing: Fit = self._categorize_sizing(attributes[3].strip())
                is_favorite: bool = len(attributes) == 5

                self.items[self.curr].append(ClothingItem(name, brand, colors, sizing, \
                                                          self._current_category(), [], is_favorite))

        txt_file.close()

    def load_ruleset(self, filename: str = "rules.txt"):
        txt_file = open(filename, "r")

        lines = txt_file.readlines()

        curr = ""

        target = ["BRANDS", ""]

        txt_file.close()

if __name__ == "__main__":
    db: Database = Database()

    db.load_clothing_from_txt()