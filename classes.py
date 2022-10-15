

# Defines an oretype object that contains the
# name of the ore
# image for the ore type
# amount of ore we have
# coin value for 1 ore of this type


class OreType:
    def __init__(self, name=str, image=str, value=float):
        self.name = name
        self.image = image
        self.amount = 0
        self.value = value
    
    def addOre(self, amount):
        self.amount += amount

class MineType:
    def __init__(self, name=str, rates=list):
        self.name = name
        self.minerCount = 0
        self.oreRates = rates
        self.workerTimer = 0

    def mine():
        return OreType #recieved for a mine action

    def assignMiner(self):
        self.minerCount += 1

class Stat:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Upgrade:
    def __init__(self, name=str, costOres=list, costMult=float, statModified=Stat, magnitude=float, upType=str):
        self.name = name
        # List of tuples containing (cost, OreType)
        self.costOres = costOres
        self.costMult = costMult
        self.statModified = statModified
        self.count = 0
        self.magnitude = magnitude
        self.type = upType

    def buyUpgrade(self):
        for cost, ore in self.costOres:
            totCost = self.count * self.costMult * cost
            if totCost > ore.amount:
                return
        ore.value -= totCost
        self.count += 1
        if self.type == "Add":
            self.statModified.value += self.count * self.magnitude
        elif self.type == "Multiply":
            self.statModified.value *= self.count * self.magnitude

class Data:
    def __init__(self) -> None:
        pass
    
    coin = 0

    clickBaseValue = Stat("Base Click Value", 1)
    clickMulti = Stat("Click Multiplier", 1)
    minerValMulti = Stat("Miner Value Multiplier", 1)
    minerSpeedMulti = Stat("Miner Speed Multiplier", 1)
    minersAvailable = Stat("Miners Available", 0)
    minersTotal = Stat("Total Miners", 0)

    # Initializes a list of OreType objects
    ores = {
        "Copper": OreType("Copper", "", 2),
        "Iron": OreType("Iron", "", 5),
        "Silver": OreType("Silver", "", 25),
        "Gold": OreType("Gold", "", 100)
    }

    # Stores all of the mine values
    mines = {
        "Copper": MineType("Copper", [{"Ore": ores["Copper"], "Rate": 1}]),
        "Iron": MineType("Iron", [{"Ore": ores["Copper"], "Rate": 0.75}, {"Ore": ores["Iron"], "Rate": 0.25}]),
        "Silver": MineType("Silver", [{"Ore": ores["Copper"], "Rate": 0.25},{"Ore": ores["Iron"], "Rate": 0.50}, {"Ore": ores["Silver"], "Rate": 0.25}]),
        "Gold": MineType("Gold", [{"Ore": ores["Copper"], "Rate": 0.10}, {"Ore": ores["Iron"], "Rate": 0.20}, {"Ore": ores["Silver"], "Rate": 0.40}, {"Ore": ores["Gold"], "Rate": 0.30}])
    }

    upgrades = {
        "Click_Multiplier": Upgrade("Click Multiplier", [(1, ores["Copper"])], 10, clickMulti, 10, "Multiply"),
        "Click_Base_Count": Upgrade("Base Click Value", [(1, ores["Copper"])], 1.2, clickBaseValue, 1, "Add")
    }

    def getOre(self, ore=str):
        return self.ores[ore]

    def getMine(self, ore=str):
        return self.mines[ore]
    
    def getUpgrade(self, upgrade=str):
        return self.upgrades[upgrade]