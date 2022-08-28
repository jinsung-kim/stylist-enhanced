from models.Models import ClothingItem

class Node:

    def __init__(self, item: ClothingItem, end: bool = False):
        """
        :param value: ClothingItem
        :param end: checks whether the current node should be the end
        """
        self.item = item
        self.end = end
        self.children = {}

    def __eq__(self, other) -> bool:
        return (self.item == other.item
                and self.end == other.end and self.children == other.children)

    def __str__(self) -> str:
        res = "Value: %s End node: %s" % (self.item, self.end)
        return res