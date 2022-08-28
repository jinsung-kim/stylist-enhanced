from Type import Color, Type, Fit, Mission, Brand

class ClothingItem:

    def __init__(self, item_name: str, brand: Brand, prim: Color, sec: Color, size: Fit, category: Type, trip_mission: list[Mission]):
        '''
        :param item_name: name of item, relatively descriptive, brand not needed
        :param brand: name of the brand
        :param prim, sec: Color type
        :param size: how the article of clothing fits
        :param category: what sort of item this is
        :param trip_mission: how this item is typically worn
        '''
        self.item_name = item_name
        self.brand = brand
        self.primary = prim
        self.secondary = sec
        self.size = size
        self.category = category
        self.trip_mission = trip_mission