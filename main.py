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
                            newLocation.items.append(newItem)
                except KeyError:
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

            # 3 - Check for items #
            if self.player.location.checkForItems():
                print("There are items here!")

            # 4 - User prompt #
            self.command(input("\n---> What now? "))
            input()

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
        if len(user) == 1 and user[0] == "take":
            itemToTake = input("\tTake what (ID)? ")
            try:
                self.player.inventory[int(itemToTake)] = self.player.location.items[int(itemToTake)]
                print("\tTook the", self.player.location.items[int(itemToTake)].name + ".")
                # Remove from location items #
                del self.player.location.items[int(itemToTake)]
            except KeyError:
                print("Can't find that item.")
        elif len(user) > 1 and user[0] == "take":
            # User has given the ID of an item #
            try:
                self.player.inventory[int(user[1])] = self.player.location.items[int(user[1])]
                print("\tTook the", self.player.location.items[int(user[1])].name + ".")
                # Remove from location items #
                del self.player.location.items[int(user[1])]
            except KeyError:
                print("Can't find that item.")

        # INV #
        if user[0] == "inv":
            self.player.displayInventory()


class Location:
    def __init__(self, id_num, name):
        self.id = id_num
        self.name = name
        self.items = []

    def checkForItems(self):
        if len(self.items) > 0:
            return True
        else:
            return False

    def displayItems(self):
        for item in self.items:
            print("-"*len(item.description) + "-")
            print(item.id, "-", item.name)
            print(item.description)
            print("-"*len(item.description) + "-")
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
            print(self.inventory[item].id, "-", self.inventory[item].name)
            print(self.inventory[item].description)
            print("-"*len(self.inventory[item].description) + "-")
        if len(self.inventory) == 0:
            print("You don't have any items.")

class Item:
    def __init__(self, id_num, itemName, itemDescription):
        self.id = id_num
        self.name = itemName
        self.description = itemDescription

MainGame = Game()
MainGame.gameLoop()
input()
