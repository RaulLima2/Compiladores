class table_symbol:
    __table = {}

    def __init__(self, key, val):
        if key != None and val != None:
            self.__table = {key:val}
        else:
            self.__table = {}
    def put(self, key, val):
        self.__table.update({key:val})
    
    def get(self, key):
        return self.__table.get(key)
    
    def contains(self, key, value) -> bool:
        return self.__table.get(key) != None 

    def p(self):
        print(self.__table)
    
    


    