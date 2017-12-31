"""
 Little Big Adventure Meta Language Demo

 Very simple game engine to interpretate the LBAML
 By Rasmus Westerlin, Apps'n Downs, December 2017

 Locations are interlinked and used to create the game world
"""
import json,sqlite3

from inventory import *

dbname = "story.db"

def get_location_file(id):
    ret = None
    with open(str(id)+".json","r") as f:
        jsontext = f.read();
        d = json.loads(jsontext)
        d['id']=id
        return Location(**d)

def get_location(id):
    ret = None
    con = sqlite3.connect(dbname)
    for row in con.execute("SELECT json FROM gamebase WHERE id=?",(id,)):
        jsontext = row[0];
        d = json.loads(jsontext)
        d['id']=id
        ret = Location(**d)
        break
    con.close()
    return ret

class Location():

    def __init__(self,id=0,name="A location",description="Bare location. Here is nothing",neighbors=[],items={}):
        self.id = id
        self.name = name
        self.description = description
        self.neighbors = neighbors
        self.items = items
        self.environment = Inventory()
        self.environment.populate(self.items)

    def neighbor(self,direction):
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            return None

    def update(self):
        self.environment.update() # updates all items in location
        subenvs = self.environment.getsubcontainers(self) # updates all items in other items
        for subenv in subenvs:
            subenv.update()
        con = sqlite3.connect(dbname)
        jsonDictionary = {"name":self.name,"description":self.description,
        "neighbors":self.neighbors,"items":self.environment.output()}
        jsontext = json.dumps(jsonDictionary)
        con.execute("INSERT OR REPLACE INTO gamebase(id,json) VALUES(?,?)",(self.id,jsontext))
        con.commit()

    def getExits(self):
        output =""
        exits = list(self.neighbors.keys())
        for exit in exits:
            output += exit + sepSign(exit,exits,"or")
        if output == "": output = "Nowhere..    "
        return  output

    def __str__(self):
        lines = [self.name]
        lines += wrapper(self.description+"\n",width=72)
        lines += wrapper(str("You see: %s" %self.environment+"\n"),width=72)
        lines += wrapper(str("You can go: %s" %self.getExits()),width=72)
        output = ""
        for line in lines:
            output += line + "\n"
        return output

    def addItem(self,item):
        self.environment.add(item)

    def removeItem(self,item,andSubItems=False):
        self.environment.remove(item)
        if andSubItems:
            subs = self.environment.getsubcontainers(self)
            for sub in subs:
                sub.remove(item)
