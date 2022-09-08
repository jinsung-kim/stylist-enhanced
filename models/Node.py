from __future__ import annotations
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.Models import ClothingItem

class Node:

    def __init__(self, clothing_item: ClothingItem):
        self.item: ClothingItem = clothing_item
        self.children: list[Node] = []

    def add_adj(self, adj: list[Node]):
        for item in adj:
            self.children.append(item)
