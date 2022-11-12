from numpy.random import choice
# Defines an oretype object that contains the
# name of the ore
# image for the ore type
# amount of ore we have
# coin value for 1 ore of this type


#lisst meant to contain the possible suffixes for number scaling
numScaleList = ["", "K", "M", "B", "t", "q", "Q", "s", "S", "o", "n", "d", "U", "D", "T", "Qt", "Qd", "Sd", "St", "O", "N", "v", "c"]

#scales the numbers appropriately for the wallet to look nice
def numberScaling(input):
    x = input
    amount = 0
    while x >= 1000 or x <=-1000:
        x = x / 1000
        amount += 1
    return str(round(x, 2)) + numScaleList[amount]

class OreType:
    def __init__(self, name:str, image:str, value:float, colMod:float):
        self.name = name
        self.image = image
        self.amount = 0
        self.value = value
        self.collectionModifier = colMod

    def setAmount(self, amount):
        self.amount = amount

    def getName(self):
        return self.name
    
    def getImage(self):
        return self.image
    
    def getCollectionModifier(self):
        return self.collectionModifier

    def getAmount(self):
        return self.amount
    
    def getValue(self):
        return self.value
    
    def addOre(self, amount):
        self.amount += amount

class OreRate:
    def __init__(self, oreType:OreType, rate:float):
        self.ore = oreType
        self.rate = rate

    def getOre(self):
        return self.ore
    
    def getRate(self):
        return self.rate

class MineType:
    def __init__(self, name:str, rates:list, unlocked:bool, unlockCost:int=0):
        self.name = name
        self.minerCount = 0
        self.oreRates = rates
        self.unlocked = unlocked
        self.unlockCost = unlockCost
    
    def getName(self):
        return self.name
    
    def getMinerCount(self):
        return self.minerCount
    
    def getOreRates(self):
        return self.oreRates

    def assignMiners(self, x):
        self.minerCount += x
    
    def unassignMiners(self, x):
        self.minerCount -= x

    def getUnlockCost(self):
        return self.unlockCost

    def isUnlocked(self):
        return self.unlocked

    def unlock(self):
        self.unlocked = True

class Stat:
    def __init__(self, name, value, toReset):
        self.name = name
        self.value = value
        self.toReset = toReset
    
    def getName(self):
        return self.name
    
    def getValue(self):
        return self.value

    def setValue(self, x):
        self.value = x

class Upgrade:
    def __init__(self, name:str, costOres:list, costMult:float, statModified:Stat, magnitude:float, upType:str, cap:int):
        self.name = name
        # List of OreRate objects
        self.costOres = costOres
        self.costMult = costMult
        self.statModified = statModified
        self.count = 0
        self.magnitude = magnitude
        self.type = upType
        self.cap = cap
    
    def getCost(self):
        sellRate = []
        for rate in self.costOres:
            if self.type == "Add":
                totCost = (self.count+1) * self.costMult * rate.getRate()
            elif self.type == "Multiply":
                totCost = pow((self.costMult * rate.getRate()), (self.count+1)) 
            sellRate.append(OreRate(rate.getOre(), round(totCost, 2)))
        return sellRate

    def getCostString(self):
        if self.cap > 0 and self.count >= self.cap:
            return "Upgrade Maxed"
        costString = "Cost: "
        for rate in self.getCost():   
            costString += numberScaling(rate.getRate()) + " " + rate.getOre().getName()
        return costString

    def getName(self):
        return self.name

    def getEffect(self):
        mod = ""
        if self.type == "Add" and self.magnitude > 0:
            mod = "+"
        if self.type == "Mutiply":
            mod = "x"
        return mod + numberScaling(self.count * self.magnitude * 100) + "%"

    def getStatModified(self):
        return self.statModified
    
    def getCount(self):
        return self.count

    def getMagnitude(self):
        return self.magnitude
    
    def getType(self):
        return self.type

    def getCap(self):
        return self.cap

    def setCap(self, x):
        self.cap = x

    def canAfford(self):
        for rate in self.getCost():
            if rate.getRate() > rate.getOre().getAmount():
                return False
        return True

    def buyUpgrade(self):
        if self.canAfford() and (self.cap < 0 or self.count < self.cap):
            for rate in self.getCost():
                rate.getOre().addOre(-rate.getRate())
            self.count += 1
            if self.type == "Add":
                self.statModified.value += self.magnitude
            elif self.type == "Multiply":
                self.statModified.value *= self.magnitude

class StatHolder:
    def __init__(self):
        self.gameStats = [
            Stat("Base Click Value", 1, True), #Note: true is for reset on retire, and false is dont reset on retire
            Stat("Click Multiplier", 1, True), 
            Stat("Miner Value Multiplier", 1, True), 
            Stat("Miners Available", 0, True), 
            Stat("Total Miners", 0, True), 
            Stat("Miner Speed", 100, True),
            Stat("Miner Time Upgradable", 100, True),
            Stat("Miner Cost Reduce", 1.0, True),
            Stat("Total Clicks", 0, False),
            Stat("Total Coin Earned", 0, False),
            Stat("Time Played", 0, False),
            Stat("Total Copper Earned", 0, False),
            Stat("Total Iron Earned", 0, False),
            Stat("Total Silver Earned", 0, False),
            Stat("Total Gold Earned", 0, False),
            Stat("Total Diamond Earned", 0, False) 
        ]
    
    def adjustStat(self, statName:str, amount:float):
        pass
    
    def dumpStats(self):
        statDump = {}
        for stat in self.gameStats:
            statDump[stat.getName()] = stat.getValue()
        return statDump

    def getStat(self, statName:str):
        for stat in self.gameStats:
            if statName == stat.getName():
                return stat
        return None

class Data:
    def __init__(self) -> None:
        self.coin = OreType("Coin", "", 0, 1)

        self.stats = StatHolder()

        self.minerTimer = 0

        # Initializes a list of OreType objects
        self.ores = {
            "Copper": OreType("Copper", "", 2, 1),
            "Iron": OreType("Iron", "", 5, 0.25),
            "Silver": OreType("Silver", "", 25, 0.05),
            "Gold": OreType("Gold", "", 100, 0.001),
            "Diamond": OreType("Diamond", "", 500, 0.00001)
        }

        # Stores all of the mine values
        self.mines = {
            "Copper": MineType("Copper", [OreRate(self.ores["Copper"], 1)], True),
            "Iron": MineType("Iron", [OreRate(self.ores["Copper"], 0.75), OreRate(self.ores["Iron"], 0.25)], False, 1000),
            "Silver": MineType("Silver", [OreRate(self.ores["Copper"], 0.25), OreRate(self.ores["Iron"], 0.50), OreRate(self.ores["Silver"], 0.25)], False, 100000000),
            "Gold": MineType("Gold", [OreRate(self.ores["Copper"], 0.10), OreRate(self.ores["Iron"], 0.20), OreRate(self.ores["Silver"], 0.40), OreRate(self.ores["Gold"], 0.30)], False, 1000000000000000000000),
            "Diamond": MineType("Diamond", [OreRate(self.ores["Iron"], 0.10), OreRate(self.ores["Silver"], 0.20), OreRate(self.ores["Gold"], 0.35), OreRate(self.ores["Diamond"], 0.35)], False, 10000000000000000000000000000000000)
        }

        self.MINE_ORDER = ["Copper", "Iron", "Silver", "Gold", "Diamond"]

        self.upgrades = {
            "Click_Multiplier": Upgrade("Click Multiplier", [OreRate(self.ores["Copper"], 1)], 10, self.getStat("Click Multiplier"), 10, "Multiply", -1),
            "Click_Base_Count": Upgrade("Base Click Value", [OreRate(self.ores["Copper"], 1)], 1.2, self.getStat("Base Click Value"), 1, "Add", -1),
            "Miner_Speed": Upgrade("Miner Speed Reduction", [OreRate(self.ores["Copper"], 1)], 1.2, self.getStat("Miner Speed"), -5, "Add", 19),
            "Miner_Cost": Upgrade("Miner Cost Multiplier", [OreRate(self.ores["Copper"], 1)], 1.2, self.getStat("Miner Cost Reduce"), 0.5, "Multiply", 1)
        }

        self.activeMine = self.mines["Copper"]

    def getOre(self, ore:str):
        return self.ores[ore]

    def getStat(self, statName:str):
        return self.stats.getStat(statName)

    def getMine(self, ore:str):
        return self.mines[ore]

    def getUpgrade(self, upgrade:str):
        return self.upgrades[upgrade]

    def getAllMines(self):
        mineList = []
        for ore, mine in self.mines.items():
            mineList.append(mine)
        return mineList

    #if the player has enough coins, buy the next Miner
    def buyMiner(self):
        cost = pow(10, self.getStat("Total Miners").getValue() + 1)
        if self.coin.getAmount() >= (cost * self.getStat("Miner Cost Reduce").getValue()):
            self.getStat("Total Miners").value += 1
            self.getStat("Miners Available").value += 1
            self.coin.addOre(-cost * self.getStat("Miner Cost Reduce").getValue())

    #if the player has enough miners available, assign x miners to the mine given.
    def assignMiners(self, mine:MineType, x:int=1):
        available = self.getStat("Miners Available").getValue()
        if available >= x:
            mine.assignMiners(x)
            self.getStat("Miners Available").setValue(available - x)
        else:
            mine.assignMiners(available)
            self.getStat("Miners Available").setValue(0)

    #Player unassignes all miners of a specific mine.
    def unassignAllMiners(self, mine:MineType):
        self.getStat("Miners Available").setValue(self.getStat("Miners Available").getValue() + mine.getMinerCount())
        mine.unassignMiners(mine.getMinerCount())
        

    #if there is one, set activeMine to the mine after the current activeMine
    def setNextMine(self):
        index = self.MINE_ORDER.index(self.activeMine.getName())+1
        if not index >= len(self.MINE_ORDER):
            mine = self.getMine(self.MINE_ORDER[index])
            if mine.isUnlocked():
                self.activeMine = mine
            else:
                self.unlockMine(mine)

    #returns next mine, if there is not one, return None
    def getNextMine(self):
        index = self.MINE_ORDER.index(self.activeMine.getName())+1
        if not index >= len(self.MINE_ORDER):
            return self.getMine(self.MINE_ORDER[index])
        else:
            return None

    #if there is one, set activeMine to the mine before the current activeMine.
    def setPreviousMine(self):
        index = self.MINE_ORDER.index(self.activeMine.getName())-1
        if not index < 0:
            self.activeMine = self.getMine(self.MINE_ORDER[index])
    
    #returns next mine, if there is not one, return None
    def getPreviousMine(self):
        index = self.MINE_ORDER.index(self.activeMine.getName())-1
        if not index < 0:
            return self.getMine(self.MINE_ORDER[index])
        else:
            return None

    #sells ratio * ore.amount for coins
    # 1 <= ratio < 0
    def sellOre(self, ore:OreType, ratio:float):
        oreLeft = ore.getAmount() * (1-ratio)
        oreSold = ore.getAmount() * ratio
        ore.setAmount(oreLeft)
        self.getStat("Total Coin Earned").setValue(self.getStat("Total Coin Earned").getValue() + oreSold * ore.getValue())
        self.coin.addOre(oreSold * ore.getValue())

    def getMinerValue(self, mine:MineType, ore:OreType):
        return self.getStat("Miner Value Multiplier").getValue() * mine.getMinerCount() * ore.getCollectionModifier()
        
    def getClickValue(self, ore:OreType=None):
        if ore:
            return self.getStat("Base Click Value").getValue() * self.getStat("Click Multiplier").getValue() * ore.getCollectionModifier()
        else:
            return self.getStat("Base Click Value").getValue() * self.getStat("Click Multiplier").getValue()

    #Commits mine action on mine passed in
    def mineAction(self, mine:MineType, isMiner=False):
        ore = []
        probability = []
        for rate in mine.getOreRates():
            ore.append(rate.getOre())
            probability.append(rate.getRate())
        obtainedOre = choice(ore, p=probability)
        if isMiner:
            obtainedOre.amount += self.getMinerValue(mine, obtainedOre)
            if obtainedOre.getName() == "Copper":
                self.getStat("Total Copper Earned").setValue(self.getStat("Total Copper Earned").getValue() + (self.getMinerValue(mine, obtainedOre)))
            elif obtainedOre.getName() == "Iron":
                self.getStat("Total Iron Earned").setValue(self.getStat("Total Iron Earned").getValue() + (self.getMinerValue(mine, obtainedOre)))
            elif obtainedOre.getName() == "Silver":
                self.getStat("Total Silver Earned").setValue(self.getStat("Total Silver Earned").getValue() + (self.getMinerValue(mine, obtainedOre)))
            elif obtainedOre.getName() == "Gold":
                self.getStat("Total Gold Earned").setValue(self.getStat("Total Gold Earned").getValue() + (self.getMinerValue(mine, obtainedOre)))
            elif obtainedOre.getName() == "Diamond":
                self.getStat("Total Diamond Earned").setValue(self.getStat("Total Diamond Earned").getValue() + (self.getMinerValue(mine, obtainedOre)))
        else: 
            obtainedOre.amount += self.getClickValue(obtainedOre)
            if obtainedOre.getName() == "Copper":
                self.getStat("Total Copper Earned").setValue(self.getStat("Total Copper Earned").getValue() + (self.getClickValue(obtainedOre)))
            elif obtainedOre.getName() == "Iron":
                self.getStat("Total Iron Earned").setValue(self.getStat("Total Iron Earned").getValue() + (self.getClickValue(obtainedOre)))
            elif obtainedOre.getName() == "Silver":
                self.getStat("Total Silver Earned").setValue(self.getStat("Total Silver Earned").getValue() + (self.getClickValue(obtainedOre)))
            elif obtainedOre.getName() == "Gold":
                self.getStat("Total Gold Earned").setValue(self.getStat("Total Gold Earned").getValue() + (self.getClickValue(obtainedOre)))
            elif obtainedOre.getName() == "Diamond":
                self.getStat("Total Diamond Earned").setValue(self.getStat("Total Diamond Earned").getValue() + (self.getClickValue(obtainedOre)))


    #makes the miners work
    def work(self):
        if self.minerTimer >= (self.getStat("Miner Speed").getValue()): #Make sure to cap
            for key, mine in self.mines.items():
                if mine.getMinerCount() > 0:
                    self.mineAction(mine, True)
            self.minerTimer = 0
        else:
            self.minerTimer += 1

    def unlockMine(self, mine:MineType):
        if self.coin.getAmount() >= mine.getUnlockCost():
            self.coin.addOre(-mine.getUnlockCost())
            mine.unlock()

    def dataLoad(self, data:dict):
        self.coin.setAmount(data["Coins"])
        for mineName, count in data["Miners Assigned"].items():
            self.getMine(mineName).assignMiners(count)
        for mineName, unlock in data["Mines Unlocked"].items():
            if unlock:
                self.getMine(mineName).unlock()
        for oreName, amount in data["Ores"].items():
            self.getOre(oreName).addOre(amount)
        for name, count in data["Upgrades"].items():
            self.getUpgrade(name).count = count
        self.activeMine = self.getMine(data["Active Mine"])
        for statName, value in data["Stats"].items():
            self.getStat(statName).setValue(value)
        

    def dataDump(self):
        data = {}

        data["Miners Assigned"] = {}
        data["Mines Unlocked"] = {}
        data["Coins"] = self.coin.getAmount()
        for name, mine in self.mines.items():
            data["Mines Unlocked"][name] = mine.isUnlocked()
            data["Miners Assigned"][name] = mine.getMinerCount()
        data["Ores"] = {}
        for key, ore in self.ores.items():
            data["Ores"][key] = ore.getAmount()
        data["Upgrades"] = {}
        for name, upgrade in self.upgrades.items():
            data["Upgrades"][name] = upgrade.getCount()
        data["Active Mine"] = self.activeMine.getName()
        data["Stats"] = self.stats.dumpStats()
        return data