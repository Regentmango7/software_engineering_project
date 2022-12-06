# MINE CLICKER GAME
import pygame
import Colors
import classes
import json
import os
import math
from classes import numberScaling
pygame.init()

MINE_SCREEN = 0
SMITH_SCREEN = 1
CONTRACT_SCREEN = 2
RETIRE_SCREEN = 3
STAT_SCREEN = 4

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
#create screen, background, framerate, and font
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Click Miners")
background = Colors.gray
framerate = 60
font = pygame.font.Font("freesansbold.ttf", 16)
timer = pygame.time.Clock()

gameData = classes.Data()

#flags for which screen we are on
activeScreen = 0

mineList = gameData.getAllMines()



#draws in the wallet, which contains the ore amount and coin amount
def drawWallet():
    pygame.draw.rect(screen, Colors.baige, (10, 10, 300, 55))
    totCoin = font.render("Coins: " + numberScaling(gameData.coin.getAmount()), True, Colors.black)
    screen.blit(totCoin, (15, 15))
    totCopper = font.render("Copper: " + numberScaling(gameData.getOre("Copper").getAmount()), True, Colors.black)
    screen.blit(totCopper, (15, 30))
    totIron = font.render("Iron: " + numberScaling(gameData.getOre("Iron").getAmount()), True, Colors.black)
    screen.blit(totIron, (15, 45))
    totSilver = font.render("Silver: " + numberScaling(gameData.getOre("Silver").getAmount()), True, Colors.black)
    screen.blit(totSilver, (150, 15))
    totGold = font.render("Gold: " + numberScaling(gameData.getOre("Gold").getAmount()), True, Colors.black)
    screen.blit(totGold, (150, 30))
    totDiamond = font.render("Diamond: " + numberScaling(gameData.getOre("Diamond").getAmount()), True, Colors.black)
    screen.blit(totDiamond, (150, 45))

def drawButton(title:str, x:int, y:int):
    swapArea = pygame.draw.circle(screen, Colors.black, (x, y), 30, 30)
    text = font.render(title, True, Colors.white)
    screen.blit(text, (x, y))
    return swapArea

#draws in the mine clicking area, and displays the ores per click
def drawMine():
    mineArea = pygame.draw.circle(screen, Colors.black, (SCREEN_WIDTH/2, SCREEN_HEIGHT/5*3), 90, 90) #The click circle to generate ores
    screen.blit(font.render(numberScaling(gameData.getClickValue()), True, Colors.white), (SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/5*3))
    return mineArea, drawMineSwitcher(gameData.getNextMine(), SCREEN_WIDTH/2 + 120, SCREEN_HEIGHT/4*3), drawMineSwitcher(gameData.getPreviousMine(), SCREEN_WIDTH/2 - 300, SCREEN_HEIGHT/4*3)

#draws in the upgrade circle
def drawUpgrade(upgrade:classes.Upgrade, x:float, y:float):
    upgradeArea = pygame.draw.rect(screen, Colors.oreColors[upgrade.currentTier], (x - 55, y - 28, 250, 70)) 
    screen.blit(font.render("Cost: " + upgrade.getCostString(), True, Colors.black), (x-20, y))
    screen.blit(font.render("Effect: " + str(upgrade.getEffect()), True, Colors.black), (x-20, y + 20))
    screen.blit(font.render(upgrade.getName(), True, Colors.black), (x-20, y-20))
    return upgradeArea

def drawMineSwitcher(mine, x, y): 
    if mine:
        mineSwitch = pygame.draw.rect(screen, Colors.black, (x, y, 180, 55))
        if mine.isUnlocked():
            screen.blit(font.render("Go to " + mine.getName() + " mine", True, Colors.white), (x + 5, y + 20))
        else:
            screen.blit(font.render("Unlock " + mine.getName() + " mine", True, Colors.white), (x + 5, y + 5))
            screen.blit(font.render("Cost: " + numberScaling(mine.getUnlockCost()) + " Coins", True, Colors.white), (x + 5, y + 35))
        return mineSwitch


def drawLabel(labelString:str, x:int, y:int):
    pygame.draw.rect(screen, Colors.baige, (x, y, 130, 60))
    screen.blit(font.render(labelString, True, Colors.black), (x+65/2, y+25))


#draws in the conversion circle
def drawConversion(oreName:str, x:int, y:int, color):
    #Displays how many coins you get for 1 Ore
    pygame.draw.rect(screen, Colors.black, (x, y, 110, 40))
    screen.blit(font.render("1 " + oreName + " -> " , True, Colors.white), (x+5, y+5))
    screen.blit(font.render(str(gameData.getOre(oreName).getValue()) + " Coins", True, Colors.white), (x+5, y+20))

    #Sell 10% ore button and label
    sellTenPercent = pygame.draw.rect(screen, color, (x+120, y, 80, 40))
    screen.blit(font.render("Sell 10%", True, Colors.black), (x+125, y+5))
    screen.blit(font.render(oreName, True, Colors.black), (x+125, y+20))
    #Sell 50% ore button and label
    sellFiftyPercent = pygame.draw.rect(screen, color, (x+210, y, 80, 40))
    screen.blit(font.render("Sell 50%", True, Colors.black), (x+215, y+5))
    screen.blit(font.render(oreName, True, Colors.black), (x+215, y+20))
    #Sell all ore button and label
    sellAll = pygame.draw.rect(screen, color, (x+300, y, 80, 40)) #The click circle to sell ores and gain coins
    screen.blit(font.render("Sell All" , True, Colors.black), (x+305, y+5))
    screen.blit(font.render(oreName, True, Colors.black), (x+305, y+20))

    

    return sellTenPercent, sellFiftyPercent, sellAll



def drawUpgradesHeader():
    drawLabel("Upgrades", (SCREEN_WIDTH * 3) / 4, 100)
    #pygame.draw.rect(screen, Colors.black, ((SCREEN_WIDTH * 3) / 4 - 165, 150, 25, 100))
    #screen.blit((font.render("Total Miners: " + numberScaling(gameData.getStat("Total Miners").getValue()), True, Colors.black)), (SCREEN_WIDTH/2 - 95, 155))


#draws in the circles to buy miners and assign miners, displays miner counts.
def drawMinerButtons(mineName:str, y:float, color):
    pygame.draw.rect(screen, color, (SCREEN_WIDTH/2 - 210, y - 5, 360, 50))
    screen.blit((font.render(mineName, True, Colors.black)), (SCREEN_WIDTH/2 - 200, y))
    screen.blit((font.render(str(gameData.getMine(mineName).getMinerCount()), True, Colors.black)), (SCREEN_WIDTH/2 - 200, y + 25))
    #pygame.draw.rect(screen, color, (SCREEN_WIDTH/2 - 100, y - 5, 250, 60))
    
    if gameData.getMine(mineName).isUnlocked():
        oneMiner = pygame.draw.rect(screen, Colors.black, (SCREEN_WIDTH/2 - 100, y, 40, 40))
        screen.blit((font.render("1", True, Colors.white)), (SCREEN_WIDTH/2 - 85, y + 15))
        fiveMiner = pygame.draw.rect(screen, Colors.black, (SCREEN_WIDTH/2 - 32.5, y, 40, 40))
        screen.blit((font.render("5", True, Colors.white)), (SCREEN_WIDTH/2 - 17.5, y + 15))
        twentyFiveMiner = pygame.draw.rect(screen, Colors.black, (SCREEN_WIDTH/2 + 32.5, y, 40, 40))
        screen.blit((font.render("25", True, Colors.white)), (SCREEN_WIDTH/2 + 47.5, y + 15))
        unAssignMiner = pygame.draw.rect(screen, Colors.green, (SCREEN_WIDTH/2 + 100, y, 40, 40))
        screen.blit((font.render("U", True, Colors.white)), (SCREEN_WIDTH/2 + 115, y + 15))
        return oneMiner, fiveMiner, twentyFiveMiner, unAssignMiner
    else: 
        screen.blit((font.render("Unlock This Mine First", True, Colors.black)), (SCREEN_WIDTH/2 - 85, y + 15))
        return None, None, None, None

def drawBuyMinerButtons(y:float):
    drawLabel("Miners", SCREEN_WIDTH/2 - 95, 100)
    screen.blit((font.render("Miner Cost: " + str(numberScaling(gameData.getMinerCost())), True, Colors.black)), (SCREEN_WIDTH/2 - 100, y-30))
    pygame.draw.rect(screen, Colors.black, (SCREEN_WIDTH/2 - 210, y - 5, 360, 50))
    screen.blit((font.render("Buy Miners", True, Colors.white)), (SCREEN_WIDTH/2 - 200, y))
    screen.blit((font.render(numberScaling(gameData.getStat("Miners Available").getValue()), True, Colors.white)), (SCREEN_WIDTH/2 - 200, y+25))
    numberScaling(gameData.getStat("Miners Available").getValue())
    oneMiner = pygame.draw.rect(screen, Colors.red, (SCREEN_WIDTH/2 - 100, y, 40, 40))
    screen.blit((font.render("1", True, Colors.white)), (SCREEN_WIDTH/2 - 85, y + 15))
    fiveMiner = pygame.draw.rect(screen, Colors.red, (SCREEN_WIDTH/2 - 32.5, y, 40, 40))
    screen.blit((font.render("5", True, Colors.white)), (SCREEN_WIDTH/2 - 17.5, y + 15))
    twentyFiveMiner = pygame.draw.rect(screen, Colors.red, (SCREEN_WIDTH/2 + 32.5, y, 40, 40))
    screen.blit((font.render("25", True, Colors.white)), (SCREEN_WIDTH/2 + 47.5, y + 15))
    unassignAll = pygame.draw.rect(screen, Colors.green, (SCREEN_WIDTH/2 + 100, y, 40, 40))
    screen.blit((font.render("U", True, Colors.white)), (SCREEN_WIDTH/2 + 115, y + 15))
    #assignMiner = pygame.draw.circle(screen, Colors.blue, (50, 150), 20, 20)
    #screen.blit((font.render("Assign Miner", True, Colors.white)), (50-20, 150-20))
    #screen.blit((font.render(numberScaling(gameData.getMine(mineName).getMinerCount()), True, Colors.white)), (50, 150))
    return oneMiner, fiveMiner, twentyFiveMiner, unassignAll


#modify for one function
def drawContract1(contract):
    cont1 = pygame.draw.rect(screen, Colors.baige, (10, 200, 200, 55))
    title = font.render("Contract 1", True, Colors.black)#font.render("Coins: " + numberScaling(gameData.coin.getAmount()), True, Colors.black)
    cost = font.render("Cost: " + str(contract.getCostString()) + " " + str(contract.getCostType().getName()), True, Colors.black)
    payout = font.render("Payout: " + str((contract.getPayoutString())), True, Colors.black)
    screen.blit(title, (15, 205))
    screen.blit(cost, (15, 220))
    screen.blit(payout, (15, 235))
    return cont1

def drawContract2(contract):
    cont2 = pygame.draw.rect(screen, Colors.baige, (10, 300, 200, 55))
    title = font.render("Contract 2", True, Colors.black)#font.render("Coins: " + numberScaling(gameData.coin.getAmount()), True, Colors.black)
    cost = font.render("Cost: " + str(contract.getCostString()) + " " + str(contract.getCostType().getName()), True, Colors.black)
    payout = font.render("Payout: " + str((contract.getPayoutString())), True, Colors.black)
    screen.blit(title, (15, 305))
    screen.blit(cost, (15, 320))
    screen.blit(payout, (15, 335))
    return cont2

def drawContract3(contract):
    cont3 = pygame.draw.rect(screen, Colors.baige, (10, 400, 200, 55))
    title = font.render("Contract 3", True, Colors.black)#font.render("Coins: " + numberScaling(gameData.coin.getAmount()), True, Colors.black)
    cost = font.render("Cost: " + str(contract.getCostString()) + " " + str(contract.getCostType().getName()), True, Colors.black)
    payout = font.render("Payout: " + str((contract.getPayoutString())), True, Colors.black)
    screen.blit(title, (15, 405))
    screen.blit(cost, (15, 420))
    screen.blit(payout, (15, 435))
    return cont3


def drawRetire():
    retireRect = pygame.draw.rect(screen, Colors.baige, (1000, 300, 200, 55))
    title = font.render("Retire", True, Colors.black)#font.render("Coins: " + numberScaling(gameData.coin.getAmount()), True, Colors.black)
    skillz = font.render("Skill Points: " + str(gameData.skillpoint.getAmountString()), True, Colors.black)
    retire_value = font.render("Retirement Value: " + str((gameData.retire_value_string())), True, Colors.black)
    screen.blit(skillz, (1005, 335))
    screen.blit(retire_value, (1005, 320))
    screen.blit(title, (1005, 305))
    return retireRect


def handleAssignMiners(eventPos, oneMiner, fiveMiner, twentyFiveMiner, removeMiners, oreName):
    mine = gameData.getMine(oreName)
    if mine.isUnlocked():
        if oneMiner.collidepoint(eventPos):
            gameData.assignMiners(mine, 1)
        if fiveMiner.collidepoint(eventPos):
            gameData.assignMiners(mine, 5)
        if twentyFiveMiner.collidepoint(eventPos):
            gameData.assignMiners(mine, 25)
        if removeMiners.collidepoint(eventPos):
            gameData.unassignAllMiners(mine)

def handleSellers(eventPos, tenSeller, fiftySeller, allSeller, oreName):
    if tenSeller.collidepoint(eventPos):
        gameData.sellOre(gameData.getOre(oreName), 0.1)
    if fiftySeller.collidepoint(eventPos):
        gameData.sellOre(gameData.getOre(oreName), 0.5)
    if allSeller.collidepoint(eventPos):
        gameData.sellOre(gameData.getOre(oreName), 1)

def save():
    print("Game is closed")

    dataDump = gameData.dataDump()

    with open("./local_data.json", "w") as saveFile:
        json.dump(dataDump, saveFile, indent=4)

    print("Game is Saved")
if os.path.exists("./local_data.json"):
    with open("./local_data.json", "r") as file:
        gameData.dataLoad(json.load(file)) 
if __name__ == "__main__":
    # Main body of code
    toChangeScreen = 0
    tfChangeScreen = False
    tfChangeMine = False
    running = True
    while running:
        timer.tick(framerate)
        gameData.getStat("Time Played").setValue(gameData.getStat("Time Played").getValue() + (timer.get_time()/1000.0))
        for event in pygame.event.get():
            #quits the game
            if event.type == pygame.QUIT:
                save()
                running = False
            if activeScreen == MINE_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #gives the player ore based on the ore per click amount multiplied by the multiplier
                    if mineArea.collidepoint(event.pos):
                        gameData.getStat("Total Clicks").setValue(gameData.getStat("Total Clicks").getValue() + 1)
                        gameData.mineAction(gameData.activeMine)
                    #increases the base ore per click
                    
                    if gameData.getPreviousMine() and previousMine.collidepoint(event.pos):
                        tfChangeMine = True
                        mineChange = "PREV"
                    if gameData.getNextMine() and nextMine.collidepoint(event.pos):
                        tfChangeMine = True
                        mineChange = "NEXT"
                    if swapScreenToSmith.collidepoint(event.pos):
                        toChangeScreen = SMITH_SCREEN
                        tfChangeScreen = True
                    
                    if swapScreenToStats.collidepoint(event.pos):
                        toChangeScreen = STAT_SCREEN
                        tfChangeScreen = True

                    #Contracts
                    if cont1.collidepoint(event.pos):
                        gameData.buyContract(gameData.contracts["Contract1"], gameData.contracts["Contract1"].getCostType().getAmount())
                    if cont2.collidepoint(event.pos):
                        gameData.buyContract(gameData.contracts["Contract2"], gameData.contracts["Contract2"].getCostType().getAmount())
                    if cont3.collidepoint(event.pos):
                        gameData.buyContract(gameData.contracts["Contract3"], gameData.contracts["Contract3"].getCostType().getAmount())

                    #retirement
                    if retire.collidepoint(event.pos):
                        gameData.execute_retire()
                            

            if activeScreen == SMITH_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #COPPER SELL HANDLERS
                    handleSellers(event.pos, sellTenPercentCopper, sellFiftyPercentCopper, sellAllCopper, "Copper")
                    #IRON SELL HANDLERS
                    handleSellers(event.pos, sellTenPercentIron, sellFiftyPercentIron, sellAllIron, "Iron")
                    #GOLD SELL HANDLERS
                    handleSellers(event.pos, sellTenPercentGold, sellFiftyPercentGold, sellAllGold, "Gold")
                    #SILVER SELL HANDLERS
                    handleSellers(event.pos, sellTenPercentSilver, sellFiftyPercentSilver, sellAllSilver, "Silver")
                    #DIAMOND SELL HANDLERS
                    handleSellers(event.pos, sellTenPercentDiamond, sellFiftyPercentDiamond, sellAllDiamond, "Diamond")
                    if oneMiner.collidepoint(event.pos):
                        gameData.buyMiner()
                    if fiveMiner.collidepoint(event.pos):
                        for x in range(5):
                            gameData.buyMiner()
                    if twentyFiveMiner.collidepoint(event.pos):
                        for x in range(25):
                            gameData.buyMiner()
                    if unassignAll.collidepoint(event.pos):
                        for mine in gameData.getAllMines():
                            gameData.unassignAllMiners(mine)
                    #COPPER Assign HANDLERS
                    handleAssignMiners(event.pos, oneMinerCopper, fiveMinerCopper, twentyFiveMinerCopper, removeCopper, "Copper")
                    #IRON Assign HANDLERS
                    handleAssignMiners(event.pos, oneMinerIron, fiveMinerIron, twentyFiveMinerIron, removeIron, "Iron")
                    #SILVER Assign HANDLERS
                    handleAssignMiners(event.pos, oneMinerSilver, fiveMinerSilver, twentyFiveMinerSilver, removeSilver, "Silver")
                    #GOLD Assign HANDLERS
                    handleAssignMiners(event.pos, oneMinerGold, fiveMinerGold, twentyFiveMinerGold, removeGold, "Gold")
                    #DIAMOND Assign HANDLERS
                    handleAssignMiners(event.pos, oneMinerDiamond, fiveMinerDiamond, twentyFiveMinerDiamond, removeDiamond, "Diamond")
                    if clickBaseUpgrade.collidepoint(event.pos):
                        gameData.getUpgrade("Click_Base_Count").buyUpgrade()
                    #decreases coin amount by 10, and increases the multiplier by one (buys an incerase in a multipier for 10 coins)
                    if clickMultUpgrade.collidepoint(event.pos):
                        gameData.getUpgrade("Click_Multiplier").buyUpgrade()
                    if workSpeed.collidepoint(event.pos):
                        gameData.getUpgrade("Miner_Speed").buyUpgrade()
                    if workCost.collidepoint(event.pos):
                        gameData.getUpgrade("Miner_Cost").buyUpgrade()
                    if workValue.collidepoint(event.pos):
                        gameData.getUpgrade("Miner_Multiplier").buyUpgrade()
                    if swapScreenToMine.collidepoint(event.pos):
                        toChangeScreen = MINE_SCREEN
                        tfChangeScreen = True
            if activeScreen == STAT_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if swapScreenToMine.collidepoint(event.pos):
                        toChangeScreen = MINE_SCREEN
                        tfChangeScreen = True
            if tfChangeScreen:
                activeScreen = toChangeScreen
                tfChangeScreen = False
            if tfChangeMine:
                if mineChange == "NEXT":
                    gameData.setNextMine()
                if mineChange == "PREV":
                    gameData.setPreviousMine()
                tfChangeMine = False

        # OUTSIDE EVENT LOOP
        if activeScreen == MINE_SCREEN:
            #draws a series of objects
            screen.fill(background)
            drawWallet()
            drawLabel(gameData.activeMine.getName(), (SCREEN_WIDTH/2 - 65), (SCREEN_HEIGHT/4))
            mineArea, nextMine, previousMine = drawMine()
            swapScreenToSmith = drawButton("To Smithing", 600, 600)
            swapScreenToStats = drawButton("To Stats", 700, 600)
            cont1 = drawContract1(gameData.contracts["Contract1"])
            cont2 = drawContract2(gameData.contracts["Contract2"])
            cont3 = drawContract3(gameData.contracts["Contract3"])
            retire = drawRetire()
        if activeScreen == SMITH_SCREEN:
            screen.fill(background)
            drawWallet()
            #SELLERS
            drawLabel("Sell Ores", 125, 100)
            sellTenPercentCopper, sellFiftyPercentCopper, sellAllCopper = drawConversion("Copper", 25, 200, Colors.copper)
            sellTenPercentIron, sellFiftyPercentIron, sellAllIron = drawConversion("Iron", 25, 250, Colors.iron)
            sellTenPercentSilver, sellFiftyPercentSilver, sellAllSilver = drawConversion("Silver", 25, 300, Colors.silver)
            sellTenPercentGold, sellFiftyPercentGold, sellAllGold = drawConversion("Gold", 25, 350, Colors.gold)
            sellTenPercentDiamond, sellFiftyPercentDiamond, sellAllDiamond = drawConversion("Diamond", 25, 400, Colors.diamond)

            oneMiner, fiveMiner, twentyFiveMiner, unassignAll = drawBuyMinerButtons(200)
            oneMinerCopper, fiveMinerCopper, twentyFiveMinerCopper, removeCopper = drawMinerButtons("Copper", 275, Colors.copper)
            oneMinerIron, fiveMinerIron, twentyFiveMinerIron, removeIron = drawMinerButtons("Iron", 350, Colors.iron)
            oneMinerSilver, fiveMinerSilver, twentyFiveMinerSilver, removeSilver = drawMinerButtons("Silver", 425, Colors.silver)
            oneMinerGold, fiveMinerGold, twentyFiveMinerGold, removeGold = drawMinerButtons("Gold", 500, Colors.gold)
            oneMinerDiamond, fiveMinerDiamond, twentyFiveMinerDiamond, removeDiamond = drawMinerButtons("Diamond", 575, Colors.diamond)

            drawLabel("Upgrades", (SCREEN_WIDTH * 3) / 4, 100)
            clickBaseUpgrade = drawUpgrade(gameData.getUpgrade("Click_Base_Count"), (SCREEN_WIDTH * 3) / 4, 220)
            clickMultUpgrade = drawUpgrade(gameData.getUpgrade("Click_Multiplier"), (SCREEN_WIDTH * 3) / 4, 300)
            workSpeed = drawUpgrade(gameData.getUpgrade("Miner_Speed"), (SCREEN_WIDTH * 3) / 4, 380)
            workCost = drawUpgrade(gameData.getUpgrade("Miner_Cost"), (SCREEN_WIDTH * 3) / 4, 460)
            workValue = drawUpgrade(gameData.getUpgrade("Miner_Multiplier"), (SCREEN_WIDTH * 3) / 4, 540)

            swapScreenToMine = drawButton("To Mine", 100, 600)
        if activeScreen == CONTRACT_SCREEN:
            pass
        if activeScreen == STAT_SCREEN:
            screen.fill(background)
            screen.blit(font.render("Total Clicks: " + numberScaling(gameData.getStat("Total Clicks").getValue()), True, Colors.white), (700, 100)) #TO move
            screen.blit(font.render("Total Coins: " + numberScaling(gameData.getStat("Total Coin Earned").getValue()), True, Colors.white), (700, 200)) #TO move
            screen.blit(font.render("Seconds played: " + numberScaling(gameData.getStat("Time Played").getValue()), True, Colors.white), (700, 300)) #TO move
            screen.blit(font.render("Total Copper Earned: " + numberScaling(gameData.getStat("Total Copper Earned").getValue()), True, Colors.white), (700, 400)) #TO move
            screen.blit(font.render("Total Iron Earned: " + numberScaling(gameData.getStat("Total Iron Earned").getValue()), True, Colors.white), (950, 100)) #TO move
            screen.blit(font.render("Total Silver Earned: " + numberScaling(gameData.getStat("Total Silver Earned").getValue()), True, Colors.white), (950, 200)) #TO move
            screen.blit(font.render("Total Gold Earned: " + numberScaling(gameData.getStat("Total Gold Earned").getValue()), True, Colors.white), (950, 300)) #TO move
            screen.blit(font.render("Total Diamond Earned: " + numberScaling(gameData.getStat("Total Diamond Earned").getValue()), True, Colors.white), (950, 400)) #TO move
            swapScreenToMine = drawButton("To Mine", 700, 600)
        if activeScreen == RETIRE_SCREEN:
            pass


        gameData.work()

        pygame.display.flip()

pygame.quit()