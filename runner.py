from __future__ import annotations
import sys
import os
import copy
import time
import requests
from decouple import config
from threading import Thread

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.KeyValueStore import KeyValueStore
from models.Node import Node
from models.Models import *

CATEGORIES: list[str] = ["HATS", "OUTERWEAR", "TOPS", "BOTTOMS", "SHOES"]
API_KEY: str = config("WEATHER_KEY")

class Database:
    
    def __init__(self, location: str = "Millbrae", weather_on: bool = False) -> None:
        # Each category organized
        self.items: dict[str, list[Node]] = {}
        self.ruleset: dict[str, KeyValueStore] = {}
        self.seen_outfits: list[list[ClothingItem]] = []
        self.nodes_start: list[Node] = []
        self.curr: str = ""
        self.location: str = location
        self.temperature_f: float = 70
        self.weather_on: bool = weather_on

        if self.weather_on:
            self._return_weather()

    def _generate_brand(self, text: str) -> Brand:
        split_brands: list[str] = text.split("/")
        main_brand: str = split_brands[0]
        collab: bool = True if len(split_brands) > 1 else False
        split_brands.pop(0)
        return Brand(main_brand, collab, split_brands)

    def _generate_colors(self, text: str) -> list[Color]:
        split_str: list[str] = text.split("/")
        colors: list[Color] = []

        for color in split_str:
            if "-" in color: # Faded color
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

    def _returnType(self, text: str) -> list[any]:
        line_split: list[str] = text.split("->")
        value: int = int(text.split("=")[1].strip())
        one: any = None
        two: any = None
        if self.curr == "FIT":
            one = self._categorize_sizing(line_split[0].strip())
            two = self._categorize_sizing(line_split[1].split("=")[0].strip())
        elif self.curr == "COLOR":
            one = self._generate_colors(line_split[0].strip())
            two = self._generate_colors(line_split[1].split("=")[0].strip())
        # To add combo later
        else:
            pass
        return [one, two, value]

    def load_clothing_from_txt(self, filename: str = "rotation.txt") -> bool:
        txt_file = open(filename, "r")

        lines = txt_file.readlines()

        target = ["HATS", "OUTERWEAR", "TOPS", "BOTTOMS", "SHOES"]
        adding_clothing = False

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
                is_favorite: bool = (len(attributes) == 5)

                self.items[self.curr].append(Node(ClothingItem(name, brand, colors, sizing, \
                                                          self._current_category(), [], is_favorite)))

        self._add_connections()

        txt_file.close()

    def load_ruleset_from_txt(self, filename: str = "ruleset.txt"):
        txt_file = open(filename, "r")

        lines = txt_file.readlines()
        target = ["FIT", "COLOR"]
        adding = False

        for line in lines:
            line = line.strip("\n")
            if line in target:
                self.curr = line
                self.ruleset[self.curr] = KeyValueStore(self.curr)
                adding = True
            elif len(line) == 0:
                self.curr = ""
                adding = False
            elif len(line) > 0 and adding:
                parsed: list[any] = self._returnType(line)
                if self.curr == "COLOR":
                    self.ruleset[self.curr].store(parsed[0][0], parsed[1][0], parsed[2])
                else:
                    self.ruleset[self.curr].store(parsed[0], parsed[1], parsed[2])

        txt_file.close()

    def _add_connections(self):
        for item in self.items[CATEGORIES[0]]:
            item.add_adj(self.items[CATEGORIES[1]])
            item.add_adj(self.items[CATEGORIES[2]])
            self.nodes_start.append(item)

        # Starting nodes from outerwear, tops
        for i in range(1, 3):
            for item in self.items[CATEGORIES[i]]:
                self.nodes_start.append(item)

        # Connect each category with the next until the shoes
        for i in range(1, 4):
            for item in self.items[CATEGORIES[i]]:
                item.add_adj(self.items[CATEGORIES[i + 1]])

    def _dfs(self, curr: Node, outfit: list[ClothingItem]):
        outfit.append(curr.item)
        if curr.item.category == Category.shoes: # Last item
            if outfit not in self.seen_outfits:
                self.seen_outfits.append(copy.deepcopy(outfit))
        else:
            for next_node in curr.children:
                self._dfs(next_node, outfit)
        outfit.pop()

    def _outfit_count(self) -> dict[int, int]:
        res: dict[int, int] = {}

        for outfit in self.seen_outfits:
            if len(outfit) not in res:
                res[len(outfit)] = 1
            else:
                res[len(outfit)] += 1
        
        return res

    def generate_outfits(self, top_k: int) -> list[list[ClothingItem]]:

        threads: list[Thread] = []

        for node in self.nodes_start:
            t = Thread(target=self._dfs, args=(node, [],))
            threads.append(t)
            t.start()

        # Wait for all to finish
        for t in threads:
            t.join()

        scored: list[tuple[int, ClothingItem]] = []

        # Evaluate scores
        for fit in self.seen_outfits:
            scored.append((self._calculate_score(fit), fit))

        scored.sort(key=lambda y: y[0])
        scored.reverse()

        res: list[list[ClothingItem]] = []

        i: int = 0
        n: int = 0

        while (n < top_k):
            fit: list[ClothingItem] = scored[i][1]
            if (fit not in res):
                res.append(fit)
                n += 1
            i += 1

        return res

    def _calculate_score(self, outfit: list[ClothingItem]) -> int:
        final_score: int = 0

        # Go through fit ruleset to match top -> bottom
        outerwear: int = -1
        top: int = -1
        bottom: int = -1
        for i in range(len(outfit)):
            # Outerwear overrides top -> because it layers over
            if outfit[i].category == Category.top:
                top = i
            if outfit[i].category == Category.outerwear:
                outerwear = i
            if outfit[i].category == Category.pants:
                bottom = i

            # Favorite piece
            if outfit[i].is_favorite:
                final_score += 1

        if outerwear == -1:
            if self.ruleset["FIT"].exists(outfit[top].size, outfit[bottom].size):
                final_score += self.ruleset["FIT"].find(outfit[top].size, outfit[bottom].size)
        # Has outerwear
        else:
            if self.ruleset["FIT"].exists(outfit[outerwear].size, outfit[bottom].size):
                final_score += self.ruleset["FIT"].find(outfit[outerwear].size, outfit[bottom].size)
            
            # Also check to ensure that the top does not outdo the top in terms of length / size
            if outfit[top].size.value > outfit[outerwear].size.value:
                final_score -= 1
            elif outfit[top].size == outfit[outerwear].size:
                final_score += 1

            # If the weather is lower than 65 degrees, outerwear is required (basically)
            if self.temperature_f < 65.0 and self.weather_on:
                final_score += 3

        # Go through color ruleset, the main check is top -> bottom
        if outerwear == -1:
            if self.ruleset["COLOR"].exists(outfit[top].primary, outfit[bottom].primary):
                final_score += self.ruleset["COLOR"].find(outfit[top].primary, outfit[bottom].primary)
        else:
            if self.ruleset["COLOR"].exists(outfit[outerwear].primary, outfit[bottom].primary):
                final_score += self.ruleset["COLOR"].find(outfit[outerwear].primary, outfit[bottom].primary)

        # Pant to shoe combo -> all outfits will have this
        if self.ruleset["COLOR"].exists(outfit[bottom].primary, outfit[-1].primary):
            final_score += self.ruleset["COLOR"].find(outfit[bottom].primary, outfit[-1].primary)

        return final_score

    def _return_weather(self):
        WEATHER_URL: str = "http://api.weatherapi.com/v1/current.json?key=" + API_KEY + "&q=" + self.location + "&aqi=no"

        r = requests.get(WEATHER_URL)

        if (r.status_code == 200):
            self.temperature_f = float(r.json()["current"]["temp_f"])
            print("The weather in your area is " + str(self.temperature_f) +
                  "° Fahrenheit")
        else:
            print(
                "The weather could not be retrieved. Please try again later.")

    def print_outfits(self, outfits: list[list[ClothingItem]]):
        for outfit in outfits:
            for item in outfit:
                print(item)
            print()

if __name__ == "__main__":
    db: Database = Database()

    time_start: float = time.time()

    print("Generating")
    print()

    db.load_clothing_from_txt()
    db.load_ruleset_from_txt()
    db.print_outfits(db.generate_outfits(5))

    time_end: float = time.time()

    print("Generating outfits took {} seconds".format(time_end - time_start))