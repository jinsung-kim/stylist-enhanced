class KeyValueStore:
    '''
    This is for saving rulesets and applying score values
    It would be used like this:
    name -> colorSet -> key1: "black", key2: "blue", value: 1
    name -> fit -> key1: "slim", key2: "regular", value: 0.5
    '''

    def __init__(self, name: str = ""):
        self.name = name
        self.vals = {}

    @staticmethod
    def _generate_key(key1: any, key2: any) -> str:
        '''
        Keys are sorted in alphabetical order so they do not need to be stored twice
        '''
        k1: str = str(key1)
        k2: str = str(key2)
        if k1 > k2:
            return k2 + '_' + k1
        else:
            return k1 + '_' + k2

    def store(self, key1: any, key2: any, value: any):
        '''
        :param key1: first of pair
        :param key2: second of pair
        :param value: value to be returned
        '''
        self.vals[KeyValueStore._generate_key(key1, key2)] = value

    def find(self, key1: any, key2: any) -> any:
        '''
        Returns the value for the key pair if it exists
        '''
        if self.exists(key1, key2):
            return self.vals[KeyValueStore._generate_key(key1, key2)]
        return None

    def exists(self, key1: any, key2: any) -> bool:
        try:
            _ = self.vals[KeyValueStore._generate_key(key1, key2)]
            return True
        except:
            return False

    def __str__(self):
        return "Store for: {}, current count: {}".format(self.name, len(self.vals))