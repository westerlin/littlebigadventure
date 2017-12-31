# Little big adventure language
Developing a meta language for text adventures.

By applying meta language an author can create a text adventure which can be played in the Little Big adventure game engine.

### Prerequisites ###

The current implementation is compliant to Python 3.6

dependent modules:

os, sys, sqlite3, cmd, textwrap, json

### Quick start ###

To run the game you have to initialize the story. You type in your command prompt:

  `> python3.6 writestory.py`

This basically copies JSON files (meta language) to game database. If successfull, you should then be informed that story.db is created. To play the game you type:

  `> python3.6 littleadventure.py`

The demo consists for five rooms (two hidden) and 11 items. See if you can find the rusty sword and sharpen it.

### Explaination ###
Currenly based on JSON where objects like rooms and items can be defined.

 * Rooms have exits associated to other rooms. Commands like "walk", "go" are associated to the exits which are labeled directly in the room description file.
  Rooms can hold items.

 * Items have states and a command library which complements basic commands ("take","look" etc.). The commands have prerequisites and actionresponses.
    * Prerequisites checks if specific game states are fulfilled in order to carry out the action. If prerequisites are not met then the action cannot be filfulled. Each prerequisite has a failtext to inform the play of why the action could not be completed
      * Item state requirements
      * Item in inventory requirements
      * Tests of randomness
    * Action responses makes changes to the game:
      * Create/destroy room exits
      * Create/destroy items in rooms/ inventory
      * Change item states

#### Very Basic example ####

Let's go over an example how this is thought to work. Lets consider the following:

```
{
  "base":{
    "name":"rusty sword",
    "description":"Very old, rusty shortsword. Have seen its better days.",
    "state":[]
  },
  "commands":{
    "sharpen":{
      "prerequisites":[
        {"equipped":{"is":{"sharpen stone":"e8"},"failtext":"You cannot with your bare hands"}}
      ],
      "responseAction":{
          "textresponse":"You sharpen that sword some.",
          "actionpoints":-10,
          "state":{"add":"sharpened"}
      }
    }
  }
}
```

Here we define an item - a rusty sword which is code _e2_ in game. Per default all objects can be:

 * examined: Which basically displays items description (and possible items it contains if visible)
 * taken: which moves item to players inventory (maybe at some point depending on room etc.)

In this example we also define a command specific for the sword - namely __sharpen__
There are som prerequisites for doing this action. The player has to be equipped (currently the engine does not distinquish between equipped and inventory) with a sharpening stone (an item in its own right defined in code _e8_). So the play er writes:

`What is your bidding, Sire? sharpen rusty sword  `

If the does not have the sharpening stone then engine replies:

`You cannot with your bare hands  `

Which is defined in the failtext for the associated prerequisite.
If the player has the sharpening stone the engine replies:

`You sharpen that sword some  `

 And the rusty sword changes state to _sharpened_ which can be confirmed if the sword is inspected.

### Little Big command syntax ###
 The prior example points to what we would say is a complicated action (involves one action and two items). Normally in text adventures there are two ways to write these. Either you write:

 _use_ __sharpening stone__ on __rusty sword__

or

_sharpen_ __rusty sword__ with __sharpening stone__

The game engine takes the latter approach, where verb indicates what action is to be taken and on what subject. The game engine automatically runs through available tools in order to meet requirements to _sharpen_ rusty sword. Thus, in this command setting the play does not have to write the '_with..._'-part. Thereby actions requiring more than one tool (or means) can also be handled.

The problem with omitting the "with..."-part becomes evident when:

  _fill_ bottle

Because with what? Water, air or what ever substance, gas etc. which may fit into the bottle. Also we could consider a player who wants to brew a potion of some kind. There the central object is non-existent. Lets say we want to brew a potion of healing. In order to act the object needs to be available - so concepts are not possible yet in the game engine. We could however condition on a central part of the means which indicates what the player are brewing. Example:

_brew_ healing potion recipe

And then game engine will check that the ingredients: bowl, spider web, herps etc. are available.

More on this as we develop further ..

### Program files ###

The structure of the files are depicted in the dependency tree below:

  * __littleadventure.py__ (input/output and main game manager)
    * location.py (handles locations or rooms)
    * itemobject.py (handles item)
      * inventory.py (handles a stack of items)
      * commandobject.py (handles prerequisites and actionresponses)

  * __writestory.py__ (converts JSON to story.DB to be used in game engine above)

Programs in __bold__ represent main programs. All other a modules to be included.

NB! repository also include samples of JSON files which are placed in ./story subfolder


### Current issues and ideas for development ###

  - [ ] Restart game (make copy of story.db)
  - [ ] Save player status (c00 record)
 - [ ] Smarter item naming matching (old chest = chest)
  - [x] program to check integrity of JSON files
  - [x] should build an overview of references (OK - almost)
  - [x] puts JSON to DB for use (OK)
  - [ ] saving feature
   - [x] establish data base (OK)
   - [x] loading from data (OK)
   - [x] location and item object should save back (OK)
  - [ ] implementing of test (randomness) actionResponse
  - [x] new directions added on actionresponses (OK)
  - [ ] moving to new locations on actionsresponses
  - [ ] consider if environment should be kept with room
  - [ ] actionResponse death
  - [ ] actionResponse teleport
  - [ ] actionResponse win
  - [ ] prerequisites equipped item states (ei. need a _sharp_ axe)
  - [ ] equip (two hands, worn, helmet, glasses)
  - [x] inventories in item objects
  - [ ] time pauses between commands
  - [ ] status view of character
  - [ ] More extended item references - include state etc.
