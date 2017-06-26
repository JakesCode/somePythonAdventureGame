import json
from pprint import pprint

class Game:
    def __init__(self):
        self.locations = {}
        self.player = None
        self.createLocations()
        self.createPlayer()
        print("Game initialised with no problems.")

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
                            newItem = Item(id_num = itemData["items"][itemIndex]["id"], itemName = itemData["items"][itemIndex]["name"])
                            newLocation.items.append(newItem)
                except KeyError:
                    pass

                # Add to Game.locations dictionary #
                self.locations[index] = newLocation

    def createPlayer(self):
        # Create a Player object #
        self.player = Player()
        self.player.location = self.locations[self.player.position]


class Location:
    def __init__(self, id_num, name):
        self.id = id_num
        self.name = name
        self.items = []

class Player:
    def __init__(self):
        self.position = 0
        self.location = None
        self.health = 50

class Item:
    def __init__(self, id_num, itemName):
        self.id = id_num
        self.name = itemName

MainGame = Game()
input()
