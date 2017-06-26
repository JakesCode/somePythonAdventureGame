import json

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
    def __init__(self, itemName):
        self.name = itemName

MainGame = Game()
print(MainGame.locations[0].id)
input()
