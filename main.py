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

                # Add the directions to link certain locations together #
                for direction in list(data["locations"][index]["directions"].keys()):
                    newLocation.directions[direction] = data["locations"][index]["directions"][direction]

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
                                events = itemData["items"][itemIndex]["events"]
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

                # Locations can also have people - try/except block adds these too #
                try:
                    people = data["locations"][index]["people"]
                    for person in people:
                        with open('people.json') as peopleFile:
                            peopleData = json.load(peopleFile)["people"]
                            newPerson = Person(id_num=peopleData[person]["id"], name=peopleData[person]["name"], events=peopleData[person]["events"])

                            events = peopleData[person]["events"]
                            with open('events.json') as eventsFile:
                                eventsData = json.load(eventsFile)["events"]
                                # Add the linked event to the newLocation object #
                                newEvent = Event(id_num=eventsData[peopleData[person]["events"][0]]["id"], data=eventsData[peopleData[person]["events"][0]]["data"])
                                newPerson.events[person] = newEvent

                            newLocation.people.append(newPerson)
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
        print("Current Location:", self.player.location.name,"\n")
        # Draw Map #
        directionArrows = ["↑", "↓", "←", "→"]
        directionDisplay = [" ", " ", " ", " "]
        for direction in list(self.player.location.directions.keys()):
            if direction == "left":
                directionDisplay[0] = directionArrows[2]
            elif direction == "right":
                directionDisplay[3] = directionArrows[3]
            elif direction == "up":
                directionDisplay[1] = directionArrows[0]
            elif direction == "down":
                directionDisplay[2] = directionArrows[2]
        print(" ",directionDisplay[1]," ")
        print(directionDisplay[0],"*",directionDisplay[3])
        print(" ",directionDisplay[2]," ")


    def command(self, user):
        # Prevent any erroneous capitalisations #
        # Break user command into 'chunks' #
        user = user.lower().split(" ")

        # MOVE #
        if user[0] == "move":
            if user[1] in list(self.player.location.directions.keys()):
                self.player.position = self.player.location.directions[user[1]]
                print("Moved ",user[1],".", sep='')

        # LOOK #
        if user[0] == "look":
            self.player.location.displayItems()
            self.player.location.displayPeople()

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

        # TALK TO #
        try:
            if user[0] == "talk" and user[1] == "to":
                for person in range(0, len(self.player.location.people)):
                    if user[2] in list(self.player.location.people[person].name[person].lower().split(" ")):
                        for event in self.player.location.people[person].events:
                            self.player.location.people[person].runEvents()
        except IndexError:
            pass

        # INV / INVENTORY #
        if user[0] in ["inv", "inventory"]:
            self.player.displayInventory()


class Location:
    def __init__(self, id_num, name):
        self.id = id_num
        self.name = name
        self.items = {}
        self.events = {}
        self.directions = {}
        self.people = []

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
        # Events have completed - remove from events dictionary to avoid it happening multiple times #
        self.events.clear()

    def displayItems(self):
        print("----"*2,"Items","----"*2)
        for item in list(self.items.keys()):
            print(self.items[item].name)
            print(self.items[item].description,"\n")
        if not(self.checkForItems()):
            print("No items here.")
        print("-"*21 + "--")

    def displayPeople(self):
        print("\n")
        print("----"*2,"People","----"*2)
        for person in range(0, len(self.people)):
            print(self.people[person].name[person])
        print("-"*22 + "--")

class Player:
    def __init__(self):
        self.position = 2
        self.location = None
        self.inventory = {}
        self.quests = []

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
        elif eventType == "give":
            # This is where the player needs to give an item to a person #
            print("Begin give event")
            with open('give.json') as giveFile:
                giveData = json.load(giveFile)["give"][self.data[eventType]]
                NewQuest = Quest(id_num=giveData["id"], required_items=giveData["required_items"])
                print(NewQuest)

class Dialogue:
    def __init__(self, id_num, characters, data):
        self.id = id_num
        self.characters = characters
        self.data = data
        self.read()

    def read(self):
        # The ID key in the data dictionary corresponds to list indices in the self.characters list. #
        lineKeys = list(self.data.keys())
        for turn in range(0, len(self.data["lines"])):
            s("cls")
            # The person saying the line #
            lengthOfLineCalculation = len(self.data["lines"][turn]) - len(self.characters[self.data["order"][turn]])
            lengthOfLine = int(round(lengthOfLineCalculation / 2))
            if lengthOfLine*2 > 79:
                lengthOfLine = int(round(79/2))-1
            print("-"*lengthOfLine + self.characters[self.data["order"][turn]] + "-"*lengthOfLine)
            # The line #
            print(self.data["lines"][turn], "\n")
            offset = round(len(self.characters[self.data["order"][turn]])/4+1)
            input(' '*int(round(lengthOfLine+offset)) + "(cont.)")

class Person:
    def __init__(self, id_num, name, events):
        self.id = id_num
        self.name = name
        self.events = events

    def runEvents(self):
        for event in self.events:
            for singleEvent in list(event.data.keys()):
                event.execute(singleEvent)

class Quest:
    def __init__(self, id_num, required_items):
        self.id = id_num
        self.required_items = []


s("title Some Python Adventure Game")
MainGame = Game()
MainGame.gameLoop()
input()
