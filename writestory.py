"""
 Little Big Adventure Meta Language Story Writer

 Translates JSON files to sqlite3 DB to be used in game engine
 By Rasmus Westerlin, Apps'n Downs, December 2017

 Primitive user interface + game controls
"""

import sys,sqlite3,os,os.path

import json

def createDB(dbname, dirname):
    con = sqlite3.connect(dbname)
    con.execute(
    "CREATE TABLE IF NOT EXISTS gamebase(id char(10) PRIMARY KEY, json TEXT NOT NULL)"
    )
    con.commit()

    for filename in os.listdir(dirname):
        base, extension = os.path.splitext(filename)
        if extension == '.json' and base[0]=="r":
            with open(dirname+filename,'r') as f:
                jsontext = f.read()
                con.execute("INSERT OR REPLACE INTO gamebase(id,json) VALUES(?,?)",(base,jsontext))
                con.commit()
    con.execute(
    "CREATE TABLE IF NOT EXISTS stables(id char(10) PRIMARY KEY, json TEXT NOT NULL)"
    )
    con.commit()
    for filename in os.listdir(dirname):
        base, extension = os.path.splitext(filename)
        if extension == '.json' and base[0]=="e":
            with open(dirname+filename,'r') as f:
                jsontext = f.read()
                itemrecord = json.loads(jsontext)
                commands = json.dumps(itemrecord["commands"])
                con.execute("INSERT OR REPLACE INTO stables(id,json) VALUES(?,?)",(base,commands))
                con.commit()
                itembase = json.dumps(itemrecord["base"])
                con.execute("INSERT OR REPLACE INTO gamebase(id,json) VALUES(?,?)",(base,itembase))
                con.commit()
    con.close()

def viewDB(dbname):
    con = sqlite3.connect(dbname)
    print("database read")
    #print(con.execute("SELECT json FROM gamebase LIMIT 1000"))

    for row in con.execute("SELECT * FROM gamebase WHERE id='e1'"):
        jsontext=row[1]
        base = json.loads(jsontext)
        print(row[0],base.get("name"))
        print(base)
    con.close()

print("(-) Writing up the story in DB from underlying JSON files")
print("   + Expect to find them in subfolder ./story")
#print(os.listdir("./story/"))
createDB("story.db","./story/")
print("   + Database story.db created at current folder")
print("   + Text game can now be tested")
#viewDB("story.db")
