import json,sqlite3


dbname = "story.db"

def get_room_file(id):
    ret = None
    with open(str(id)+".json","r") as f:
        jsontext = f.read();
        d = json.loads(jsontext)
        d['id']=id
        return Location(**d)

def get_room(id):
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

    def neighbor(self,direction):
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            return None

    def update(self,inventory):
        con = sqlite3.connect(dbname)
        jsonDictionary = {"name":self.name,"description":self.description,
        "neighbors":self.neighbors,"items":inventory.output()}
        jsontext = json.dumps(jsonDictionary)
        con.execute("INSERT OR REPLACE INTO gamebase(id,json) VALUES(?,?)",(self.id,jsontext))
        con.commit()
