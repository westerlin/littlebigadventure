"""
 Little Big Adventure Meta Language Demo

 Very simple game engine to interpretate the LBAML
 By Rasmus Westerlin, Apps'n Downs, December 2017

 ItemObject hold info on objects and some of the game mechanics 
"""
import json,sqlite3,sys
from inventory import *
from commandobject import *

dbname = "story.db"

def get_item_file(id):
    ret = None
    with open(str(id)+".json","r") as f:
        jsontext = f.read();
        d = json.loads(jsontext)
        d['id']=id
        return ItemObject(**d)

def get_item(id):
    ret = None
    con = sqlite3.connect(dbname)
    for row in con.execute("SELECT json FROM gamebase WHERE id=?",(id,)):
        jsontext = row[0];
        base = json.loads(jsontext)
        break
    for row in con.execute("SELECT json FROM stables WHERE id=?",(id,)):
        jsontext = row[0];
        cmd = json.loads(jsontext)
        break
    con.close()
    d = {}
    d['id']=id
    d['base']=base
    d['commands']=cmd
    ret = ItemObject(**d)
    return ret

default_base = {
        "name":"Unspecified object",
        "description":"Yet to be described.",
        "state":[],
        "items":{}
}

default_cmd = {
}


class ItemObject():

    def __init__(self, id="0", base=default_base,commands=default_cmd):
        self.id = id
        self.noun = base.get("name")
        self.description = base.get("description")
        self.state = safeInit(base.get("state"),[])
        #self.items = safeInit(base.get("items"),{})
        container = safeInit(base.get("container"),{})

        preqs = container.get("prerequisites")
        #print(container,preqs,container.get("prerequisites"))

        self.preqs = None
        self.items = None
        if preqs is not None:
            print("object",id)
            self.preqs = Prerequisites(self,preqs)


            items = safeInit(container.get("items"),{})
            self.items = Inventory()
            self.items.populate(items)

        self.plural = safeInit(base.get("plural"),False)

        #self.special = safeInit(base.get("special"),{})
        self.cmds = safeInit(commands,{})

    def getItems(self,controller):
        if self.preqs is not None:
            flag, msg = self.preqs.verify(controller)
            if flag:
                if self.items.count()>0:
                    return self.items
                else:
                    return None
            else:
                return None
        else:
            return None

    def update(self):
        con = sqlite3.connect(dbname)
        jsonDictionary = {"name":self.noun,"description":self.description,
        "state":self.state,"plural":self.plural}

        #"items":self.items.output()

        container = {}
        if self.items is not None:
            container["items"] = self.items.output()
        if self.preqs is not None:
            container["prerequisites"] = self.preqs.prerequisites
        if container != {}:
            jsonDictionary["container"] = container

        jsontext = json.dumps(jsonDictionary)
        con.execute("INSERT OR REPLACE INTO gamebase(id,json) VALUES(?,?)",(self.id,jsontext))
        con.commit()

    def getdescription(self,controller):
        output = self.description
        if len(self.state)>0:
            if self.plural:
                output += " They are "
            else:
                output += " It is "
            output += doCommaSentence(self.state)
        containerItems = self.getItems(controller)
        if containerItems is not None:
            output += "\n"
            if self.plural:
                output += "They contain: "
            else:
                output += "It contains: "
            output += str(containerItems) #doCommaSentence(list(self.items.keys()))
        #if self.preqs is not None:
        #    flag, msg = self.preqs.verify(controller)
        #    output+= "\nCheck of {} with result {} as {}".format(self.id,flag,msg)
        #    output+=str(self.preqs.prerequisites)
        return output

    def getCommand(self,command):
        return self.cmds.get(command)

    def addstate(self,states):
        if isinstance(states, str):
            if states not in self.state: self.state.append(states)
        else:
            for state in states:
                if state not in self.state: self.state.append(state)

    def removestate(self,states):
        if isinstance(states, str):
            if states in self.state: self.state.remove(states)
        else:
            for state in states:
                if state in self.state: self.state.remove(state)

    def isState(self,state):
        return state in self.state

    def isNotState(self,state):
        return state not in self.state
