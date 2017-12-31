"""
 Little Big Adventure Meta Language Demo

 Very simple game engine to interpretate the LBAML
 By Rasmus Westerlin, Apps'n Downs, December 2017

 Primitive user interface + game controls
"""
import cmd
from location import *
from itemobject import *
#from inventory import *
#from commandobject import *

class Game(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        cmd.Cmd.prompt = "What is your bidding, Sire? "
        self.inventory = Inventory()
        self.gotoLocation("r1")
        self.actionpoints = 500
        #self.focus = self.environment.get("old chest")
        #print (item[0].special.get("container"))
        #print (item[0].special.get("container").output())

    def gotoLocation(self,locationID):
        self.loc = get_location(locationID)
        self.look()

    def do_inventory(self,arg):
        """ list all inventory items """
        #print(self.inventory)
        self.respond(""+str(self.inventory))

    def do_quit(self, args):
        """Leaves the game"""
        print("Thank you for playing")
        return True

    def do_exit(self,args):
        """Leaves the game"""
        print("Thank you for playing")
        return True


    def move(self,dir):
        newlocation = self.loc.neighbor(dir)
        if newlocation is None:
            print("Sorry, you cannot go that way")
        else:
            #self.loc = get_room(newroom)
            self.updateall()
            self.gotoLocation(newlocation)
            self.look()

    def updateall(self):
        self.inventory.update()
        self.loc.update()

    def look(self):
        cls()
        print(self.loc)
        #print(self.environment.get(self,"old chest")[0].items.count())

    def addItem(self,locationId,newItems):
        if locationId == self.loc.id:
            location = self.loc
        else:
            location = get_location(roomId)
        for key in newItems.keys():
            itemid = newItems.get(key)
            item = get_item(itemid)
            location.addItem(item)
        location.update()

    def removeItem(self,locationId,newItems):
        if locationId == self.loc.id:
            location = self.loc
        else:
            location = get_location(locationId)
        for key in newItems.keys():
            itemid = newItems.get(key)
            item = get_item(itemid)
            location.removeItem(item)
        location.update()

    def addExit(self,locationId,newExits):
        if locationId == self.loc.id:
            location = self.loc
        else:
            location = get_location(locationId)
        for key in newExits.keys():
            location.neighbors[key] = newExits.get(key)
        location.update()

    def removeExit(self,locationId,newExits):
        if locationId == self.loc.id:
            location = self.loc
        else:
            location = get_location(locationId)
        for key in newExits.keys():
            location.neighbors.pop(key,None)
        location.update()

    def respond(self,responsetext):
        #for lines in textwrap.wrap(responsetext,72,replace_whitespace=False):
        #    print(lines)
        lines = wrapper(responsetext,indent=5,width=60)
        for line in lines:
            print(line)

    def isEquipped(self,itemref):
        for key in itemref.keys():
            invref = self.inventory.items.get(itemref.get(key))
            if invref is not None:
                self.respond("You use your {}".format(invref.item.noun))
                return True
        return False

    def do_look(self, args):
        """Looks at items and environment"""
        if len(args)==0:
            self.look()
        else:
            item = self.getUniqueItem(args,[self.loc.environment,self.inventory])
            if item is not None:
                self.respond("The {}:\n{}".format(item.noun,item.getdescription(self)))
        return False

    def getUniqueItem(self,itemnoun,inventories):
        items = []
        for inventory in inventories:
            items += inventory.get(self,itemnoun)
            if len(items)>0: break
        if len(items) == 1:
            return items[0]
        elif len(items)==0:
            print("I don't see the %s here .." %itemnoun)
            return None
        else:
            alternatives = ""
            for item in items:
                print("alternative items:",items)
                alternatives += item.noun
                alternatives += sepSign(item,items,"or")
            print("What {} do you mean? {} ?".format(itemnoun,alternatives))
            return None

    def updateActionPoints(self,actionpoints):
        self.actionpoints += actionpoints

    def do_move(self,args):
        """Moving around from location to location"""
        self.move(args)

    def do_walk(self,args):
        """Moving around from location to location"""
        self.move(args)

    def do_go(self,args):
        """Moving around from location to location"""
        self.move(args)

    def handleItemActions(self,item,command):
        cmdScheme = item.getCommand(command)
        if cmdScheme is None:
            return False
        else:
            ref = cmdScheme.get("reference")
            if ref is None:
                preqs = safeInit(cmdScheme.get("prerequisites"),{})
                resp  = safeInit(cmdScheme.get("responseAction"),{})
                cmdObj = CommandObject(item,preqs,resp)
                result = cmdObj.execute(self)
                return result
            else:
                return self.handleItemActions(item,ref)
        return False


    def genericDo(self,cmd,args,defaultAction=False,inventory=[]):
        if len(inventory) == 0: inventory = [self.loc.environment]
        item = self.getUniqueItem(args,inventory)
        if item is None:
            return None
        elif self.handleItemActions(item,cmd):
            return None
        else:
            if not defaultAction:
                print("You cannot {} the {}".format(cmd,args))
            return item

    def do_push(self,args):
        """ push an object """
        self.genericDo("push",args)

    def do_pull(self,args):
        """ pull an object """
        self.genericDo("pull",args)

    def do_get(self,args):
        """ get an object """
        item = self.genericDo("get",args,True)
        if item is not None:
            #item is found but not handled
            #default actions
            self.inventory.add(item)
            self.loc.removeItem(item,True)
            self.respond("You took the {}".format(item.noun))

    def do_take(self,args):
        """ take an object """
        self.do_get(args)

    def do_close(self,args):
        """ close an object """
        self.genericDo("close",args)

    def do_open(self,args):
        """ open an object """
        self.genericDo("open",args)

    def do_break(self,args):
        """ break an object """
        self.genericDo("break",args)

    def do_picklock(self,args):
        """ picklock an object """
        self.genericDo("picklock",args)

    def do_unlock(self,args):
        """ unlock an object """
        self.genericDo("unlock",args)

    def do_chop(self,args):
        self.genericDo("chop",args)

    def do_cut(self,args):
        self.genericDo("cut",args)

    def do_mine(self,args):
        self.genericDo("mine",args)

    def do_mix(self,args):
        self.genericDo("mix",args)

    def do_craft(self,args):
        self.genericDo("craft",args)

    def do_sharpen(self,args):
        self.genericDo("sharpen",args,False,[self.inventory])

    def do_drop(self,args):
        """ drop an object """
        item = self.genericDo("drop",args,True,[self.inventory])
        if item is not None:
            #item is found but not handled
            #default actions
            self.inventory.remove(item)
            self.loc.addItem(item)
            self.respond("You dropped the {}".format(item.noun))

if __name__ == "__main__":
    cls()
    g = Game()
    g.cmdloop()
