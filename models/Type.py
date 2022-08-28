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

class Type(enum.Enum):

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
        self.brand = brand
        self.collab = collab
        self.collaborators = collaborators

    def __eq__(self, other: Brand):
        if (self.brand != other.brand):
            return False
        if (self.collab != other.collab):
            return False
        return collections.Counter(self.collaborators) == collections.Counter(other.collaborators)
        

class Color:

    def __init__(self, primary: str, faded: bool = False):
        self.primary = primary
        # Faded colors should be treated like a slightly different color
        # i.e. black faded t-shirt
        self.faded = faded

    def __str__(self):
        return "Color: {}".format(self.primary)

    def __eq__(self, other: Color) -> bool:
        return (self.primary == other.primary) and (self.faded == other.faded)

    def score_compatibility(self, other) -> float:
        pass

    def convert_to_hex(self) -> str:
        pass