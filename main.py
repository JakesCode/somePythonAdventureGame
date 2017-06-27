import json
from os import system as s

class Game:
    def __init__(self):
        self.locations = {}
        self.player = None
        self.createLocations()
        self.createPlayer()

    def createLocations(self):
        # Iterates through locations.json, dynamically creates Location objects, adds to Game.locations dictionary #
        with open('locations.json') as dataFile:
            data = json.load(dataFile)
            for index in range(0, len(data["locations"])):
                newLocation = Location(id_num = data["locations"][index]["id"], name = data["locations"][index]["name"])

                # Some locations have items - try/except block scans locations and adds them to Location objects #
                try:
                    itemsToAdd = data["locations"][index]["items"]
                    with open('items.json') as itemsFile:
                        itemData = json.load(itemsFile)
                        for itemIndex in itemsToAdd:
                            # Create Item object(s) #
                            newItem = Item(id_num = itemData["items"][itemIndex]["id"], itemName = itemData["items"][itemIndex]["name"], itemDescription = itemData["items"][itemIndex]["description"])

                            # Some items have events, too. #
                            try:
                                events = data["locations"][index]["events"]
                                for event in events:
                                    # 'event' will be an ID that corresponds to an ID in the events.json file #
                                    with open('events.json') as eventsFile:
                                        eventsData = json.load(eventsFile)["events"]
                                        # Add the linked event to the newLocation object #
                                        newEvent = Event(id_num=eventsData[event]["id"], data=eventsData[event]["data"])
                                        newItem.events[event] = newEvent
                            except:
                                pass
                        newLocation.items[newItem.name.lower()] = newItem

                except KeyError:
                    pass

                # Some locations have events - try/except block scans locations and adds them to Location objects #
                try:
                    events = data["locations"][index]["events"]
                    for event in events:
                        # 'event' will be an ID that corresponds to an ID in the events.json file #
                        with open('events.json') as eventsFile:
                            eventsData = json.load(eventsFile)["events"]
                            # Add the linked event to the newLocation object #
                            newEvent = Event(id_num=eventsData[event]["id"], data=eventsData[event]["data"])
                            newLocation.events[event] = newEvent
                except:
                    pass

                # Add to Game.locations dictionary #
                self.locations[index] = newLocation

    def createPlayer(self):
        # Create a Player object #
        self.player = Player()
        self.player.location = self.locations[self.player.position]

    def gameLoop(self):
        while True:
            # Beginning of loop - Clear Screen #
            s("cls")

            # 1 - Update player location #
            self.player.location = self.locations[self.player.position]

            # 2 - Display HUD #
            self.HUD()

            # 3 - Check for items #
            #if self.player.location.checkForItems():
            #    print("There are items here!")

            # 4 - Check for events at this location #
            if self.player.location.checkForEvents():
                self.player.location.runEvents()
                # Add the HUD again #
                s("cls")
                self.HUD()

            # 5 - User prompt #
            self.command(input("\n---> What now? "))
            input()

    def HUD(self):
        print("Current Location:", self.player.location.name)
        print(self.player.health, "HP")
        print("Map:", end=' ')
        gameMap = list("-"*len(self.locations))
        for x in range(0, len(gameMap)):
            if x == self.player.position:
                print("*", end="")
            else:
                print(gameMap[x], end="")
        print("\n")

    def command(self, user):
        # Prevent any erroneous capitalisations #
        # Break user command into 'chunks' #
        user = user.lower().split(" ")

        # MOVE #
        if user[0] == "move":
            if user[1] == "left":
                if self.player.position == 0:
                    print("Can't move left!")
                else:
                    self.player.advance(-1)
            elif user[1] == "right":
                if self.player.position+1 == len(self.locations):
                    print("Can't move right!")
                else:
                    self.player.advance(1)

        # LOOK #
        if user[0] == "look":
            self.player.location.displayItems()

        # TAKE #
        if user[0] == "take":
            # Search for item in location #
            keyList = list(self.player.location.items.keys())
            for item in keyList:
                item = item.lower()
                individualElements = item.split(' ')
                try:
                    if user[1] in individualElements:
                        # Item may be linked to an event - check for this #
                        if len(self.player.location.items[item].events) > 0:
                            self.player.location.items[item].runEvents()
                        # Add to inventory, remove from location #
                        self.player.inventory[item] = self.player.location.items[item]
                        del self.player.location.items[item]
                        print("Took the",self.player.inventory[item].name + ".\n")
                        print("-"*len(self.player.inventory[item].description) + "----------")
                        print(self.player.inventory[item].name)
                        print(self.player.inventory[item].description)
                        print("-"*len(self.player.inventory[item].description) + "----------\n")
                except Exception as e:
                    if len(user) == 1:
                        print("Please specify an item.")
                    else:
                        print("Can't find that item.")

        # INV / INVENTORY #
        if user[0] in ["inv", "inventory"]:
            self.player.displayInventory()


class Location:
    def __init__(self, id_num, name):
        self.id = id_num
        self.name = name
        self.items = {}
        self.events = {}

    def checkForEvents(self):
        if len(self.events) > 0:
            return True
        else:
            return False

    def checkForItems(self):
        if len(self.items) > 0:
            return True
        else:
            return False

    def runEvents(self):
        for event in self.events:
            eventKeys = list(self.events[event].data.keys())
            for singleEvent in eventKeys:
                if singleEvent == "speech":
                    self.events[event].execute(singleEvent)
        self.events.clear()

    def displayItems(self):
        for item in list(self.items.keys()):
            print("-"*len(self.items[item].description) + "-")
            print(self.items[item].name)
            print(self.items[item].description)
            print("-"*len(self.items[item].description) + "-")
        if not(self.checkForItems()):
            print("No items here.")

class Player:
    def __init__(self):
        self.position = 0
        self.location = None
        self.health = 50
        self.inventory = {}

    def advance(self, direction):
        self.position += int(direction)
        if direction == 1:
            print("Advanced to the right.")
        else:
            print("Moved to the left.")

    def displayInventory(self):
        for item in self.inventory:
            print("-"*len(self.inventory[item].description) + "-")
            print(self.inventory[item].name)
            print(self.inventory[item].description)
            print("-"*len(self.inventory[item].description) + "-")
        if len(self.inventory) == 0:
            print("You don't have any items.")

class Item:
    def __init__(self, id_num, itemName, itemDescription):
        self.id = id_num
        self.name = itemName
        self.description = itemDescription
        self.events = {}

    def runEvents(self):
        for event in self.events:
            eventKeys = list(self.events[event].data.keys())
            for singleEvent in eventKeys:
                if singleEvent == "speech":
                    self.events[event].execute(singleEvent)
        # Events have completed - remove from events dictionary to avoid it happening multiple times #
        self.events.clear()


class Event:
    def __init__(self, id_num, data):
        self.id = id_num
        self.data = data

    def execute(self, eventType):
        if eventType == "speech":
            # This is a dialogue event #
            with open('speech.json') as speechFile:
                speechData = json.load(speechFile)["speech"][self.id]
                DialogueEvent = Dialogue(id_num=speechData["id"], characters=speechData["characters"], data=speechData["data"])

class Dialogue:
    def __init__(self, id_num, characters, data):
        self.id = id_num
        self.characters = characters
        self.data = data
        self.read()

    def read(self):
        # The ID key in the data dictionary corresponds to list indices in the self.characters list. #
        lineKeys = list(self.data.keys())
        for turn in range(0, len(self.data)):
            for line in self.data[lineKeys[turn]]:
                s("cls")
                # The person saying the line #
                lengthOfLineCalculation = len(line) - len(self.characters[int([lineKeys[turn]][0])])
                lengthOfLine = int(round(lengthOfLineCalculation / 2))
                print("-"*lengthOfLine + self.characters[int([lineKeys[turn]][0])] + "-"*lengthOfLine)
                # The line #
                print(line, "\n")
                offset = round(len(self.characters[int([lineKeys[turn]][0])]))/4+1
                input(' '*int(round(lengthOfLine+offset)) + "(cont.)")


s("title Some Python Adventure Game")
MainGame = Game()
MainGame.gameLoop()
input()
