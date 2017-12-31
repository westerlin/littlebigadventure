# Little big adventure language
Developing a meta language for text adventures.


>__Proposal:__<br/> By applying the little big adventure meta language and game engine an author can create a text adventure game  without doing any programming and focusing solely on storyline, storytelling, puzzles and progression in the adventure. <br/>


>__Ambition:__<br/> The vocabulary should be generic to fit storyline purpose although keep an overall simple style. Game elements like mining, combat like standard RPG game should be included. NPCs and interactions should be developed - looking into natural language interpretaters for this purpose. Currently the engine uses Pythons Command module for user input, but we plan to build a more general API so this can be implemented on web pages etc.

>__Warning:__<br/> The game engine is completely old school text based. There are no fancy graphics (however, we are developing a module which may contribute with ASCII art for demo purposes).


### Prerequisites ###

The current implementation is compliant to Python 3.6

dependent modules:

<ul> os, sys, sqlite3, cmd, textwrap, json </ul>


### Quick start ###

To run the game you have to initialize the story. You type in your command prompt:

  `> python3.6 writestory.py`

This basically copies JSON files (meta language) to game database. If successfull, you should then be informed that story.db is created. To play the game you type:

  `> python3.6 littleadventure.py`

The demo consists for five locations (two hidden) and 11 items. See if you can find the rusty sword and sharpen it.

### What is the Little Big Adventure meta language? ###
Currently, it is based on JSON where game objects like locations and items can be defined.

 * __Locations__ have exits associated to other rooms. Commands like "walk", "go" are associated to the exits which are labeled directly in the room description file.
  Locations can hold items and are thus a container.

 * __Items__ can normally be taken and carried by player to other locations. Like locations, some items are also containers and can hold other items (we even plan to make items have exits associated directly to them). Moreover, items have states and an associated command library which complements basic commands ("take","look" etc.). The commands have prerequisites and action responses.
    * Prerequisites checks if specific game conditions are fulfilled in order to carry out the action. If prerequisites are not met, then the action cannot be fulfilled. Each prerequisite has a __failtext__ to inform the player of why the action could not be completed. Examples of prerequisites are:
      * Item state requirements
      * Item in inventory requirements
      * Tests of randomness
    * Action responses makes changes to the game. They provide feedback in case all prerequisites are met and changes the current state of game by expanding or reducing the options available to player. Examples of action responses are:
      * Create/destroy room exits
      * Create/destroy items in rooms/ inventory/ items (which are containers)
      * Change item states

Currently the meta language is formed in JSON but YAML is considered as this also leaves room for commenting which would be nice for an author.

#### Very Basic example ####

So what does this meta language looks like?

Let's go over an example to understand how this is thought to work. Let's consider the following:

###### Sample LBA meta language #####
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

Here we define an item - a rusty sword which is code _e2_ in game (see e2.json file). Per default all objects can be:

 * _examined_: Which basically displays items description (which includes its current state and possible items it contains)
 * _taken_: Which moves the item to players inventory (however can be overridden in items own commands etc.)

In this example we also define a command which is specific for the sword - namely __sharpen__
There are som prerequisites for doing this action. The player has to be equipped (currently the engine does not distinquish between equipped and inventory) with a sharpening stone (an item in its own right defined in code _e8_). So the player writes:

`> What is your bidding, Sire? sharpen rusty sword`

If the player does not have the sharpening stone then the engine replies:

` > You cannot with your bare hands  ` (failtext)

Which is defined in the failtext for the associated prerequisite.
If the player has the sharpening stone the engine replies:

`> You sharpen that sword some  ` (textresponse)

 And the rusty sword changes state to _sharpened_ which can be confirmed if the sword is inspected.

### Little Big command syntax ###
 The prior example points to what we would say is a complicated action (involves one action and two or more items). Normally in text adventures, there are two ways to write these.

Either tool defines the intend:
  <ul> > <b>use</b> <i>sharpening stone</i> on <i>rusty sword</strong> </i></ul>

or verb defines intend:

<ul> > <b>sharpen</b> <i>rusty sword</i> with <i>sharpening stone</i></ul>

The game engine takes the latter approach, where verb indicates what action is to be taken and on what subject. The game engine automatically runs through available tools in order to meet requirements to _sharpen_ rusty sword. Thus, in this command setting the play does not have to write the '_with..._'-part. Thereby actions requiring more than one tool (or means) can also be handled.

The problem with omitting the "with..."-part becomes evident when:

<ul> >  <b>fill</b> <i>bottle</i></ul>

Because, with what? Water, air or what ever substance, gas etc. which may fit into the bottle. Also we could consider a player who wants to brew a potion of some kind. There the central object is non-existent. Lets say we want to brew a potion of healing. In order to act the object needs to be available - so concepts are not possible yet in the game engine. We could however condition on a central part of the means which indicates what the player are brewing. Example:

<ul> > <b>brew</b> <i>healing potion recipe</i></ul>

And then game engine will check that the ingredients: bowl, spider web, herps etc. are available.

More on this as we develop further ..

### Program files ###

The structure of the files are depicted in the dependency tree below:

  * __littleadventure.py__ (input/output and main game manager)
    * location.py (handles locations or rooms)
        * _lbautils.py_ (general purpose tool)
    * itemobject.py (handles item)
      * inventory.py (handles a stack of items)
        * _lbautils.py_ (general purpose tool)
      * commandobject.py (handles prerequisites and actionresponses)
        * _lbautils.py_ (general purpose tool)

  * __writestory.py__ (converts JSON to story.DB to be used in game engine above)

Programs in __bold__ represent main programs. All other are modules which are included.

NB! repository also include samples of JSON files which are placed in ./story subfolder


### Current issues and ideas for development ###

  - [ ] Restart game (make copy of story.db)
  - [ ] Smarter item naming matching (old chest = chest) - Maybe aliases
  - [x] program to check integrity of JSON files
  - [x] should build an overview of references (OK - almost)
  - [x] puts JSON to DB for use (OK)
  - [ ] saving feature
   - [x] establish data base (OK)
   - [x] loading from data (OK)
   - [x] location and item object should save back (OK)
   - [ ] Save player status (c00 record)
  - [ ] implementing of test (randomness) actionResponse
  - [x] new directions added on actionresponses (OK)
  - [ ] moving to new locations on actionsresponses
  - [x] Environment now a part of Location class (OK)
  - [ ] actionResponse death
  - [ ] actionResponse teleport
  - [ ] actionResponse win
  - [ ] prerequisites equipped item states (ei. need a _sharp_ axe)
  - [ ] equip (two hands, worn, helmet, glasses)
  - [x] inventories in item objects
  - [ ] time pauses between commands
  - [ ] status view of character
  - [ ] More extended item references - include state etc.
