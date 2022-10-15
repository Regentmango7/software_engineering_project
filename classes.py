

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
    
    def getName(self):
        return self.name
    
    def getImage(self):
        return self.image
    
    def getAmount(self):
        return self.amount
    
    def getValue(self):
        return self.value
    
    def addOre(self, amount):
        self.amount += amount

class OreRate:
    def __init__(self, oreType=OreType, rate=float):
        self.ore = oreType
        self.rate = rate

    def getOre(self):
        return self.ore
    
    def getRate(self):
        return self.rate

class MineType:
    def __init__(self, name=str, rates=list(OreRate)):
        self.name = name
        self.minerCount = 0
        self.oreRates = rates
        self.workerTimer = 0
    
    def getName(self):
        return self.name
    
    def getMinerCount(self):
        return self.minerCount
    
    def getOreRates(self):
        return self.oreRates
    
    def getWorkerTimer(self):
        return self.workerTimer

    def mine():
        return OreType #recieved for a mine action

    def assignMiner(self):
        self.minerCount += 1

class Stat:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def getName(self):
        return self.name
    
    def getValue(self):
        return self.value

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
    
    def getCostOres(self):
        return self.costOres
    
    def getCostMult(self):
        return self.costMult
    
    def getStatModified(self):
        return self.statModified
    
    def getCount(self):
        return self.count

    def getMagnitude(self):
        return self.magnitude
    
    def getType(self):
        return self.type

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
    
    coin = OreType("Coin", "", 0)

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
        "Copper": MineType("Copper", [OreRate(ores["Copper"], 1)]),
        "Iron": MineType("Iron", [OreRate(ores["Copper"], 0.75), OreRate(ores["Iron"], 0.25)]),
        "Silver": MineType("Silver", [OreRate(ores["Copper"], 0.25), OreRate(ores["Iron"], 0.50), OreRate(ores["Silver"], 0.25)]),
        "Gold": MineType("Gold", [OreRate(ores["Copper"], 0.10), OreRate(ores["Iron"], 0.20), OreRate(ores["Silver"], 0.40), OreRate(ores["Gold"], 0.30)])
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