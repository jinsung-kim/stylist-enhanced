from __future__ import annotations
import enum
import copy
import collections

class Fit(enum.Enum):
    '''
    The goal of this enum is to ensure that combinations do not vary too much
    The silhouette should maintain relatively consistent i.e. oversized top with slim pants is a no go
    '''

    # For shoes and caps
    undefined = -1
    slim = 0
    regular = 1
    oversized = 2

class Category(enum.Enum):

    undefined = -1
    hat = 0
    top = 1
    pants = 2
    shoes = 3
    outerwear = 4
    
# Trip mission (what they are trying to accomplish)
class Mission(enum.Enum):
    
    undefined = -1
    casual = 0
    formal = 1
    active = 2

class Brand:

    def __init__(self, brand: str, collab: bool = False, collaborators: list[str] = []):
        '''
        :param brand: main brand of item, typically this will be enough
        :param collab: whether an item is a collaboration piece or not
        :param collaborators: if the prior parameter is set to true, this is where the collaborators live
        '''
        self.brand: str = brand
        self.collab: bool = collab
        self.collaborators: list[str] = collaborators

    def __eq__(self, other: Brand):
        if (self.brand != other.brand):
            return False
        if (self.collab != other.collab):
            return False
        # The reason collection is used is because the content matters, order does not
        return collections.Counter(self.collaborators) == collections.Counter(other.collaborators)
        
    def __str__(self):
        res: str = "{}".format(self.brand)
        if self.collab:
            for collab in self.collaborators:
                res += " {}".format(collab)

            return res
        else:
            return res

class Color:

    def __init__(self, primary: str, faded: bool = False):
        self.primary: str = primary
        # Faded colors should be treated like a slightly different color
        # i.e. black faded t-shirt
        self.faded: bool = faded

    def __str__(self):
        return "Color: {}{}".format(self.primary, "-faded" if self.faded else "")

    def __eq__(self, other: Color) -> bool:
        return (self.primary == other.primary) and (self.faded == other.faded)

    def score_compatibility(self, other) -> float:
        pass

    def convert_to_hex(self) -> str:
        '''
        TODO: Write this out in a way that is scalable
        '''
        pass

class ClothingItem:

    def __init__(self, item_name: str, brand: Brand, colors: list[Color], 
                 size: Fit, category: Category, trip_mission: list[Mission], favorite: bool):
        '''
        :param item_name: name of item, relatively descriptive, brand not needed
        :param brand: name of the brand
        :param prim, sec: Color type
        :param size: how the article of clothing fits
        :param category: what sort of item this is
        :param trip_mission: how this item is typically worn
        :param favorite: is this item commonly worn?
        '''
        self.item_name: str = item_name
        self.brand: Brand = brand
        self.primary: Color = colors[0]
        if (len(colors) > 1):
            self.secondary: Color = colors[1]
        else:
            self.secondary: Color = None
        self.size: Fit = size
        self.category: Category = category
        self.trip_mission: list[Mission] = trip_mission
        self.is_favorite: bool = favorite

    def __str__(self):
        return "{} {} in {}".format(self.brand.__str__(), self.item_name, self.primary)