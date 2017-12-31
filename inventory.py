
"""
 Little Big Adventure Meta Language Demo

 Very simple game engine to interpretate the LBAML
 By Rasmus Westerlin, Apps'n Downs, December 2017

 Inventory is used as container for ItemObjects
 NB! inventory for player and for locations
"""
from lbautils import *

class inventoryrecord:
    def __init__(self,item,count=1):
        self.item = item
        self.count = count

    def getWeight():
        return 0

class Inventory():

    def __init__(self):
        self.items = {}
        pass

    # adds elements to inventory
    # counting if doublets
    def add(self,items):
        if not isinstance(items,list): items = [items]
        for item in items:
            isItem = self.items.get(item.id)
            if isItem is None:
                newItem = inventoryrecord(item)
                self.items[item.id] = newItem
            else:
                isItem.count += 1

    # removes elements from inventory
    # counting if doublets
    def remove(self,items):
        if not isinstance(items,list): items = [items]
        for item in items:
            isItem = self.items.get(item.id)
            if isItem is not None:
                isItem.count -= 1
                if isItem.count <= 0:
                    self.items.pop(item.id,None)

    def count(self):
        return len(list(self.items.keys()))


    #gets all containers in itesm held by inventory
    # WARNING Recursively - so danger of endless looping
    # if circular reference
    def getsubcontainers(self,controller):
        subsctns = []
        for itemids in self.items.keys():
            record = self.items.get(itemids)
            item = record.item
            subinv = item.getItems(controller)
            if subinv is not None:
                subsctns.append(subinv)
                subsctns += subinv.getsubcontainers(controller)
        return subsctns

    # used for moving big batches from one
    # inventory to another
    def __str__(self):
        output = ""
        keylist = list(self.items.keys())
        for key in keylist:
            record = self.items.get(key)
            output += record.item.noun
            if record.count > 1:
                output += " (x%i)" %record.count
            output += sepSign(key,keylist)
        if output =="":output="(Nothing)"
        return output

    # takes dictionary and populates object
    def populate(self,dictionary):
        from itemobject import get_item
        for key in dictionary.keys():
            item = get_item(dictionary.get(key))
            self.add(item)

    # dumps object to dictionary
    def output(self):
        output = {}
        for key in self.items.keys():
            record = self.items.get(key)
            for a in range(0,record.count):
                output[record.item.noun+"_"+str(a)]=key
        return output

    # updates in DB all items contained in inventory
    def update(self):
        for key in self.items.keys():
            record = self.items.get(key)
            record.item.update()

    def get(self,controller,itemnoun):
        """
            Not sure if id key is the best here
            Maybe a list as we want advanced matching
            Maybe ok as we do use ids for internal lookup
        """
        output = []
        for key in self.items.keys():
            record = self.items.get(key)
            item = record.item
            containerItems = item.getItems(controller)
            if containerItems is not None:
                output += containerItems.get(controller,itemnoun)
            if self.isMatched(item,itemnoun):
                output.append(item)
        return output

    def isMatched(self,item, NounB):
        return item.noun == NounB or (item.plural and item.noun[-1]=="s" and item.noun[0:-1]==NounB)



"""    def move(self,source):
        self.copy(source)
        source = Inventory()

    def copy(self,source):
        for itemid in source.items.keys():
            record = source.items.get(itemid)
            isItem = self.items.get(itemid)
            if isItem is not None:
                isItem += record.count
            else:
                self.items[itemid]=record
"""
