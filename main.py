import json
from pprint import pprint

class Game:
    def __init__(self):
        self.locations = {}
        self.player = None
        self.createLocations()

    def createLocations(self):
        # Iterates through locations.json, dynamically creates Location objects, adds to Game.locations dictionary #
        with open('locations.json') as dataFile:
            data = json.load(dataFile)
            for index in range(0, len(data["locations"])):
                newLocation = Location(id_num = data["locations"][index]["id"], name = data["locations"][index]["name"])
                self.locations[index] = newLocation

                # Some locations have items - try/except block scans locations and adds them to Location objects #
                try:
                    itemsToAdd = data["locations"][index]["items"]
                    with open('items.json') as itemsFile:
                        itemData = json.load(itemsFile)
                        for index in itemsToAdd:
                            # Create Item object(s) #
                            
                except KeyError:
                    pass


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
