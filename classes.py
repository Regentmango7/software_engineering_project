from numpy.random import choice
import math
# Defines an oretype object that contains the
# name of the ore
# image for the ore type
# amount of ore we have
# coin value for 1 ore of this type


#lisst meant to contain the possible suffixes for number scaling
numScaleList = ["", "K", "M", "B", "t", "q", "Q", "s", "S", "o", "n", "d", "U", "D", "T", "Qt", "Qd", "Sd", "St", "O", "N", "v", "c"]

#scales the numbers appropriately for the wallet to look nice
def numberScaling(input, percent=False):
    if input < 0:
        return "0"
    elif input < 1000 and not percent:
        return str(int(input))
    elif input < 1 and percent:
        if percent:
            return str(round(input * 100, 2)) + "%"
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

    def retire(self):
        self.amount = 0

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
    
    def getAmountString(self):
        return numberScaling(self.getAmount())
    
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

    def retire(self):
        self.minerCount = 0
        if not self.name == "Copper":
            self.unlocked = False
            

class Stat:
    def __init__(self, name, value, toReset):
        self.name = name
        self.value = value
        self.default = value
        self.toReset = toReset
    
    def reset_stat(self):
        if self.toReset:
            self.value = self.default

    def getName(self):
        return self.name
    
    def getValue(self):
        return self.value

    def setValue(self, x):
        self.value = x

class Upgrade:
    def __init__(self, name:str, costOres:list, costBase:float, statModified:Stat, magnitude:float, upType:str, cap:int):
        self.name = name
        # List of OreRate objects
        self.costOres = costOres
        self.costMult = costBase
        self.statModified = statModified
        self.count = 0
        self.magnitude = magnitude
        self.type = upType
        self.cap = cap
        self.initialCap = cap
        self.currentTier = costOres[0].getOre().getName()


    def retire(self):
        self.count = 0
        self.currentTier = self.costOres[0].getOre().getName()
        self.cap = self.initialCap
    
    def getCost(self):
        for rate in self.costOres:
            if rate.getOre().getName() == self.currentTier:
                totCost = rate.getRate() * pow(self.costMult, self.count)
                return OreRate(rate.getOre(), round(totCost, 2))

    def getCostString(self):
        if self.cap > 0 and self.count >= self.cap:
            return "Upgrade Maxed"
        costString = ""
        rate = self.getCost() 
        costString += numberScaling(rate.getRate()) + " " + rate.getOre().getName()
        return costString

    def getName(self):
        return self.name

    def getEffect(self):
        mod = ""
        amount = self.magnitude * self.count
        if self.type == "Add" and self.magnitude > 0:
            mod = "+"
            
        if self.type == "Multiply":
            mod = "x"
            amount = pow(self.magnitude, self.count)

        return mod + numberScaling(amount, True)

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
        rate = self.getCost()
        return rate.getRate() <= rate.getOre().getAmount()
            

    def nextTier(self):
        for currency in self.costOres:
            if currency.getOre().getName() == self.currentTier and self.costOres.index(currency) < len(self.costOres) - 1:
                self.currentTier = self.costOres[self.costOres.index(currency) + 1].getOre().getName() 
                self.cap += self.initialCap
    
    def buyUpgrade(self):
        if self.canAfford() and (self.cap < 0 or self.count < self.cap):
            rate = self.getCost()
            rate.getOre().addOre(-rate.getRate())
            self.count += 1
            if self.type == "Add":
                self.statModified.value += self.magnitude
            elif self.type == "Multiply":
                self.statModified.value *= self.magnitude
            if self.count == self.cap:
                self.nextTier()

class Contract:
    def __init__(self, scaling:Stat, typeOre:str, name:str):
        self.scaling = scaling
        self.typeOre = typeOre
        self.name = name

    def getCostType(self):
        return self.typeOre
    
    def getCost(self):
        return self.getScaling() * 10
    
    def getScaling(self):
        return self.scaling.getValue()

    def getPayout(self):
        return pow(self.getScaling(), 2) * self.typeOre.getValue() / 2

    
    
    def getName(self):
        return self.name
    
    def getCostString(self):
        return numberScaling(self.getCost())

    def getPayoutString(self):
        return numberScaling(self.getPayout())

    """
    takes in player progress, and detremines how much of how high of a currency it should ask for

    so it needs player progress (use mines unlockedd), 
    needs a contracts completed number (but probably make in the event pos function thingy, and have it go into scaling)
    """

class StatHolder:
    def __init__(self):
        self.gameStats = [
            Stat("Base Click Value", 1, True), #Note: true is for reset on retire, and false is dont reset on retire
            Stat("Click Multiplier", 1, True), 
            Stat("Miner Value Multiplier", 1, True), 
            Stat("Miners Available", 0, True), 
            Stat("Total Miners", 0, True), 
            Stat("Miner Speed Multi", 1.0, True),
            Stat("Miner Cost Reduce", 1.0, True),
            Stat("Total Coin Value Gained This Retire", 0, True),
            Stat("Total Clicks", 0, False),
            Stat("Total Coin Earned", 0, False),
            Stat("Time Played", 0, False),
            Stat("Total Copper Earned", 0, False),
            Stat("Total Iron Earned", 0, False),
            Stat("Total Silver Earned", 0, False),
            Stat("Total Gold Earned", 0, False),
            Stat("Total Diamond Earned", 0, False),
            Stat("Retire Count", 0, False),
            Stat("Contract1 Scaling", 25, False), #need to change to whatever is saved
            Stat("Contract2 Scaling", 25, False), #need to change to whatever is saved
            Stat("Contract3 Scaling", 25, False),  #need to change to whatever is saved
            Stat("Retire Miner Value Multiplier", 1.0, False),
            Stat("Retire Miner Speed Multi", 1.0, False),
            Stat("Retire Miner Cost Reduce", 1.0, False),
            Stat("Retire Click Multiplier", 1.0, False),
            Stat("Retire Base Click Value", 0, False),
        ]

    def retire_stats(self):
        for stat in self.gameStats:
            stat.reset_stat()
    
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
        self.skillpoint = OreType("Skill Point", "", 0, 1)

        self.stats = StatHolder()

        self.minerTimer = 0

        # Initializes a list of OreType objects
        self.ores = {
            "Copper": OreType("Copper", "", 2, 1),
            "Iron": OreType("Iron", "", 5, 1),
            "Silver": OreType("Silver", "", 25, 1),
            "Gold": OreType("Gold", "", 100, 1),
            "Diamond": OreType("Diamond", "", 500, 1)
        }

        # Stores all of the mine values
        self.mines = {
            "Copper": MineType("Copper", [OreRate(self.ores["Copper"], 1)], True),
            "Iron": MineType("Iron", [OreRate(self.ores["Copper"], 0.75), OreRate(self.ores["Iron"], 0.25)], False, 1000000),
            "Silver": MineType("Silver", [OreRate(self.ores["Copper"], 0.25), OreRate(self.ores["Iron"], 0.50), OreRate(self.ores["Silver"], 0.25)], False, 1000000000000),
            "Gold": MineType("Gold", [OreRate(self.ores["Copper"], 0.10), OreRate(self.ores["Iron"], 0.20), OreRate(self.ores["Silver"], 0.40), OreRate(self.ores["Gold"], 0.30)], False, 1000000000000000000000),
            "Diamond": MineType("Diamond", [OreRate(self.ores["Iron"], 0.10), OreRate(self.ores["Silver"], 0.20), OreRate(self.ores["Gold"], 0.35), OreRate(self.ores["Diamond"], 0.35)], False, 10000000000000000000000000000000000)
        }

        self.MINE_ORDER = ["Copper", "Iron", "Silver", "Gold", "Diamond"]

        self.upgrades = {
            "Click_Multiplier": Upgrade("Click Multiplier", [OreRate(self.ores["Copper"], 1000), OreRate(self.ores["Iron"], 2000), OreRate(self.ores["Silver"], 2000), OreRate(self.ores["Gold"], 2000), OreRate(self.ores["Diamond"], 2000)], 5, self.getStat("Click Multiplier"), 2, "Multiply", 3),
            "Click_Base_Count": Upgrade("Base Click Value", [OreRate(self.ores["Copper"], 20), OreRate(self.ores["Iron"], 2000), OreRate(self.ores["Silver"], 2000), OreRate(self.ores["Gold"], 2000), OreRate(self.ores["Diamond"], 2000)], 1.2, self.getStat("Base Click Value"), 1, "Add", 20),
            "Miner_Speed": Upgrade("Miner Speed Reduction", [OreRate(self.ores["Copper"], 100), OreRate(self.ores["Iron"], 2000), OreRate(self.ores["Silver"], 2000), OreRate(self.ores["Gold"], 2000), OreRate(self.ores["Diamond"], 2000)], 1.5, self.getStat("Miner Speed Multi"), 0.9, "Multiply", 19),
            "Miner_Cost": Upgrade("Miner Cost Multiplier", [OreRate(self.ores["Copper"], 50), OreRate(self.ores["Iron"], 2000), OreRate(self.ores["Silver"], 2000), OreRate(self.ores["Gold"], 2000), OreRate(self.ores["Diamond"], 2000)], 100, self.getStat("Miner Cost Reduce"), 0.5, "Multiply", 1),
            "Miner_Multiplier": Upgrade("Miner Value Multiplier", [OreRate(self.ores["Copper"], 10), OreRate(self.ores["Iron"], 2000), OreRate(self.ores["Silver"], 2000), OreRate(self.ores["Gold"], 2000), OreRate(self.ores["Diamond"], 2000)], 1.5, self.getStat("Miner Value Multiplier"), 2, "Multiply", 20),
            "Pres_Click_Multiplier":Upgrade("Click Multiplier", [OreRate(self.skillpoint, 1.5)], 10, self.getStat("Retire Click Multiplier"), 5, "Multiply", -1),
            "Pres_Click_Base_Count": Upgrade("Base Click Value", [OreRate(self.skillpoint, 1.1)], 20, self.getStat("Retire Base Click Value"), 10, "Add", -1),
            "Pres_Miner_Speed": Upgrade("Miner Speed Reduction", [OreRate(self.skillpoint, 1.5)], 100, self.getStat("Retire Miner Speed Multi"), 0.5, "Multiply", -1),
            "Pres_Miner_Cost": Upgrade("Miner Cost Multiplier", [OreRate(self.skillpoint, 100)], 50, self.getStat("Retire Miner Cost Reduce"), 0.1, "Multiply", -1),
            "Pres_Miner_Multiplier": Upgrade("Miner Value Multiplier", [OreRate(self.skillpoint, 1.1)], 10, self.getStat("Retire Miner Value Multiplier"), 2, "Multiply", -1),

        }

        self.activeMine = self.mines["Copper"]

        self.contracts = {
            "Contract1": Contract(self.getStat("Contract1 Scaling"), self.random_ore(self.mostRecentlyUnlocked()), "Contract1"),
            "Contract2": Contract(self.getStat("Contract2 Scaling"), self.random_ore(self.mostRecentlyUnlocked()), "Contract2"),
            "Contract3": Contract(self.getStat("Contract3 Scaling"), self.random_ore(self.mostRecentlyUnlocked()), "Contract3")
        }

    def getContract(self, name:str):
        return self.contracts[name]

    def buyContract(self, contract:Contract, inputOre:float):
        if inputOre >= contract.getCost():
            payout = contract.getPayout()
            self.coin.addOre(payout)
            contract.getCostType().addOre(-contract.getCost())
            contract.scaling.value *= 2
            contract.typeOre = self.random_ore(self.mostRecentlyUnlocked())
            self.getStat("Total Coin Value Gained This Retire").setValue(self.getStat("Total Coin Earned").getValue() + payout)
            self.getStat("Total Coin Earned").setValue(self.getStat("Total Coin Earned").getValue() + payout)
            self.getStat(contract.getName() + " Scaling").setValue(self.contracts[contract.getName()].getScaling() * 2)

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

    def getMinerCost(self):
        return pow(10, self.getStat("Total Miners").getValue() + 1) * self.getStat("Miner Cost Reduce").getValue() * self.getStat("Retire Miner Cost Reduce").getValue()

    #if the player has enough coins, buy the next Miner
    def buyMiner(self):
        cost = self.getMinerCost()
        if self.coin.getAmount() >= (cost):
            self.getStat("Total Miners").value += 1
            self.getStat("Miners Available").value += 1
            self.coin.addOre(-cost)

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

    def getMinerValue(self, mine:MineType, ore:OreType=None):
        return self.getStat("Miner Value Multiplier").getValue() * self.getStat("Retire Miner Value Multiplier").getValue() * mine.getMinerCount()
        
    def getClickValue(self, ore:OreType=None):
        return (self.getStat("Base Click Value").getValue() + self.getStat("Retire Base Click Value").getValue()) * self.getStat("Retire Click Multiplier").getValue() * self.getStat("Click Multiplier").getValue()
    #Randomly selects ore based on the rate that the ores appears in the mine.
    def random_ore(self, mine:MineType):
        ore = []
        probability = []
        for rate in mine.getOreRates():
            ore.append(rate.getOre())
            probability.append(rate.getRate())
        return choice(ore, p=probability)

    #Commits mine action on mine passed in
    def mineAction(self, mine:MineType, isMiner=False):
        obtainedOre = self.random_ore(mine)
        if isMiner:
            obtainedOre.amount += self.getMinerValue(mine, obtainedOre)
            self.getStat("Total Coin Value Gained This Retire").setValue(self.getStat("Total Coin Value Gained This Retire").getValue() + (self.getMinerValue(mine, obtainedOre) * obtainedOre.getValue()))
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
            self.getStat("Total Coin Value Gained This Retire").setValue(self.getStat("Total Coin Value Gained This Retire").getValue() + (self.getClickValue(obtainedOre) * obtainedOre.getValue()))
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
        if self.minerTimer >= 100 * (self.getStat("Miner Speed Multi").getValue() * self.getStat("Retire Miner Speed Multi").getValue()): #Make sure to cap
            for mine in self.mines.values():
                if mine.getMinerCount() > 0:
                    self.mineAction(mine, True)
            self.minerTimer = 0
        else:
            self.minerTimer += 1

    def unlockMine(self, mine:MineType):
        if self.coin.getAmount() >= mine.getUnlockCost():
            self.coin.addOre(-mine.getUnlockCost())
            mine.unlock()

    def retire_value(self):
        coinValue = self.getStat("Total Coin Value Gained This Retire").getValue()
        if coinValue == 0:
            return 0
        return (pow(coinValue/100000, 0.25))
    
    def retire_value_string(self):
        return numberScaling(self.retire_value())

    def execute_retire(self):
        self.skillpoint.addOre(int(self.retire_value()))
        self.coin.setAmount(0)

        for mine in self.mines.values():
            mine.retire()
        for ore in self.ores.values():
            ore.retire()
        for upgrade in self.upgrades.values():
            upgrade.retire()
        self.stats.retire_stats()
        self.activeMine = self.getMine("Copper")

        self.getStat("Retire Count").value += 1

        
  

    def dataDump(self):
        data = {}

        data["Miners Assigned"] = {}
        data["Mines Unlocked"] = {}
        data["Coins"] = self.coin.getAmount()
        data["Skill Points"] = self.skillpoint.getAmount()
        for name, mine in self.mines.items():
            data["Mines Unlocked"][name] = mine.isUnlocked()
            data["Miners Assigned"][name] = mine.getMinerCount()
        data["Ores"] = {}
        for key, ore in self.ores.items():
            data["Ores"][key] = ore.getAmount()
        data["Upgrades"] = {}
        for name, upgrade in self.upgrades.items():
            data["Upgrades"][name] = {"Count": upgrade.getCount(), "Tier": upgrade.currentTier}

        data["Contracts"] = {
            "Contract1": {
                "OreType": self.getContract("Contract1").getCostType().getName(),
            },
            "Contract2": {
                "OreType": self.getContract("Contract2").getCostType().getName(),
            },
            "Contract3": {
                "OreType": self.getContract("Contract3").getCostType().getName(),
            },
        }
        

        data["Active Mine"] = self.activeMine.getName()
        data["Stats"] = self.stats.dumpStats()
        return data

    def dataLoad(self, data:dict):
        self.coin.setAmount(data["Coins"])
        self.skillpoint.setAmount(data["Skill Points"])
        for mineName, count in data["Miners Assigned"].items():
            self.getMine(mineName).assignMiners(count)
        for mineName, unlock in data["Mines Unlocked"].items():
            if unlock:
                self.getMine(mineName).unlock()
        for oreName, amount in data["Ores"].items():
            self.getOre(oreName).addOre(amount)
        for name, upgradeData in data["Upgrades"].items():
            self.getUpgrade(name).count = upgradeData["Count"]
            self.getUpgrade(name).currentTier = upgradeData["Tier"]
        self.activeMine = self.getMine(data["Active Mine"])
        for statName, value in data["Stats"].items():
            self.getStat(statName).setValue(value)

        self.getContract("Contract1").typeOre = self.getOre(data["Contracts"]["Contract1"]["OreType"])
        self.getContract("Contract2").typeOre = self.getOre(data["Contracts"]["Contract2"]["OreType"])
        self.getContract("Contract3").typeOre = self.getOre(data["Contracts"]["Contract3"]["OreType"])

    def mostRecentlyUnlocked(self):
        mineUnlocked = self.mines[self.MINE_ORDER[0]]
        i = 0
        while i < len(self.MINE_ORDER):
            if self.mines[self.MINE_ORDER[i]].isUnlocked() == False:
                print(self.MINE_ORDER[i - 1]) #testing
                mineUnlocked = self.mines[self.MINE_ORDER[i - 1]]
                i = len(self.MINE_ORDER)
            i += 1
        return mineUnlocked