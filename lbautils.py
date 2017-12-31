
"""
 Little Big Adventure Meta Language Demo

 Very simple game engine to interpretate the LBAML
 By Rasmus Westerlin, Apps'n Downs, December 2017

 General purpose tools
"""
def safeInit(element,default):
    if element is None:
        return default
    return element

def cls():
    from subprocess import call
    from platform import system
    os = system()
    if os == 'Linux' or os == 'Darwin':
        call('clear', shell = True)
    elif os == 'Windows':
        call('cls', shell = True)

def wrapper(text, indent=2, width=72):
    output = []
    lines = str(text).split("\n")
    for line in lines:
        words = line.split(" ")
        wrapped=""
        for word in words:
            if len(wrapped)+len(word)+1< width:
                wrapped += word+" "
            else:
                output.append(" "*indent + wrapped)
                wrapped = word+" "
        output.append(" "*indent + wrapped)
    return output

def doCommaSentence (somelist):
    output = ""
    for item in somelist:
            output += item
            output += sepSign(item,somelist)
    return output

def sepSign(item, items,lastword="and"):
    if len(items)>1:
        if item == items[-2]: return " "+lastword+" "
    if len(items)>0:
        if item == items[-1]:return "."
    return ", "
