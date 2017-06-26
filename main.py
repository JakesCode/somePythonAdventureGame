import json

class Game:
    def __init__(self):
        self.locations = {}
        self.player = None
        self.createPlayer()
        self.createLocations()
        self.gameLoop()

    def gameLoop(self):
        try:
            while True:
                print("Currently at", self.player.location.name)
                print("You have", self.player.health, "HP", end='\n\n')
                itemsPresent = self.player.location.checkForItems()
                if itemsPresent:
                    for singleItem in self.player.location.items:
                        print("There's a", singleItem, "here!")
                self.player.advance()
                self.player.location = self.locations[self.player.position]
                print(end='\n' + "****"*8 + '\n\n')
        except Exception as e:
            print("Reached the end!")
            #raise

    def createLocations(self):
        with open("locations.json") as jsonFile:
            data = json.load(jsonFile)
            for n in range(0, len(data["locations"])):
                self.locations[n] = Location(data["locations"][n]["name"])
                try:
                    for item in data["locations"][n]["items"]:
                        linkedID = data["locations"][self.player.position]["items"][0]["id"]
                        print(linkedID)
                        self.locations[n].items.append(
                            data["items"][linkedID]["name"]
                        )
                except Exception as e:
                    if e == KeyError:
                        pass
                    else:
                        raise

    def createPlayer(self):
        self.player = Player()


class Location:
    def __init__(self, name):
        self.name = name
        self.items = []

    def checkForItems(self):
        if(len(self.items) > 0):
            return True
        else:
            return False

class Player:
    def __init__(self):
        self.position = 0
        self.location = None
        self.health = 50

    def advance(self):
        self.position += 1

class Item:
    def __init__(self, itemName):
        self.name = itemName

MainGame = Game()
input()
