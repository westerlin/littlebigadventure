"""
 Little Big Adventure Meta Language Demo

 Very simple game engine to interpretate the LBAML
 By Rasmus Westerlin, Apps'n Downs, December 2017

 CommandObject with ResponseAction and Prereuisite modules
"""

from lbautils import *

class CommandObject():

    def __init__(self,parent=None,prerequisites={},responseAction={}):
            self.responseAction = ResponseAction(parent,responseAction)
            self.prerequisites = Prerequisites(parent,prerequisites)
            self.parent = parent

    def execute(self,controller):
        all_OK, msg = self.prerequisites.verify(controller)
        if all_OK:
            self.responseAction.response(controller)
            return True
        controller.respond(msg)
        return False

class ResponseAction():

    def __init__(self,parent,responseAction={}):
            self.responseAction = responseAction
            self.parent = parent

    def response(self,controller):
        for key in self.responseAction.keys():
            if key == "textresponse": self._doTextResponse(controller,key)
            if key == "state": self._doStateUpdate(key)
            if key == "actionpoints": self._doUpdateActionPoints(controller,key)
            if key == "exit": self._doExit(controller,key)
            if key == "item": self._doItem(controller,key)


    def _doItem(self,controller,key):
        rule = self.responseAction.get(key)
        targetid = safeInit(rule.get("target"),controller.loc.id)

        anItem = rule.get("add")
        if anItem is not None:
            controller.addItem(targetid,anItem)

        anItem = rule.get("remove")
        if anItem is not None:
            controller.removeItem(targetid,anItem)

    def _doExit(self,controller,key):
        rule = self.responseAction.get(key)
        targetid = safeInit(rule.get("target"),controller.loc.id)

        anExit = rule.get("add")
        if anExit is not None:
            controller.addExit(targetid,anExit)

        anExit = rule.get("remove")
        if anExit is not None:
            controller.removeExit(targetid,anExit)

    def _doTextResponse(self,controller,key):
        controller.respond(self.responseAction.get(key))

    def _doStateUpdate(self,key):
        stateUpdates = self.responseAction.get(key)
        for key in stateUpdates.keys():
            if key == "remove": self.parent.removestate(stateUpdates.get(key))
            if key == "add": self.parent.addstate(stateUpdates.get(key))

    def _doUpdateActionPoints(self,controller,key):
        actpts = self.responseAction.get(key)
        controller.updateActionPoints(actpts)

class Prerequisites():

    def __init__(self,parent,prerequisites={}):
            self.prerequisites = prerequisites
            self.parent = parent

    def verify(self,controller):
        all_ok = True
        for preq in self.prerequisites:
            for key in preq.keys():
                if key == "state":
                    local_ok, msg = self._verifystates(controller,preq,key)
                    all_ok = all_ok and local_ok
                if key == "test":
                    local_ok, msg = self._verifytest(controller,preq,key)
                    all_ok = all_ok and local_ok
                if key == "equipped":
                    local_ok, msg = self._verifyequip(controller,preq,key)
                    all_ok = all_ok and local_ok
            if not all_ok: return all_ok, msg
        return all_ok, "OK"


    #def _getKeySafely(self,rule,key,defaulttext="You can't for some unexplained reason"):
    #    failText = rule.get(key)
    #    if failText is not None:
    #        return failText
    #    return defaulttext


    def _verifystates(self,controller,preq,key):
        rule = preq.get(key)

        #failtext = self._getKeySafely(rule,"failtext","You can't")
        #targetid = self._getKeySafely(rule,"target",self.parent.id)
        failtext = safeInit(rule.get("failtext"),"You can't")
        targetid = safeInit(rule.get("target"),self.parent.id)

        negativeState = rule.get("not")
        if negativeState is not None:
            if self.parent.isNotState(negativeState):
                return True , "Success"
            else:
                #controller.respond(failtext)
                return False, failtext

        positiveState = rule.get("is")
        if positiveState is not None:
            if self.parent.isState(positiveState):
                return True, "Success"
            else:
                #controller.respond(failtext)
                return False,failtext

        print("Some state prerequisite was mispelled and ignored")
        print("Preq was:", rule)
        return True, "System Error"

    def _verifytest(self,controller,preq,key):
        rule = preq.get(key)
        failtext = safeInit(rule.get("failtext"),"You can't")
        return True, "Success"

    def _verifyequip(self,controller,preq,key):
        rule = preq.get(key)
        failtext = safeInit(rule.get("failtext"),"You can't")

        negativeState = rule.get("not")
        if negativeState is not None:
            if self.parent.isEquipped(negativeState):
                return True, "Success"
            else:
                #controller.respond(failtext)
                return False, failtext

        positiveState = rule.get("is")
        if positiveState is not None:
            if controller.isEquipped(positiveState):
                return True, "Success"
            else:
                #controller.respond(failtext)
                return False,failtext

        return True, "System Error"
