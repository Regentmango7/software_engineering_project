# MINE CLICKER GAME
import pygame
import Colors
import classes
import json
import os
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

#lisst meant to contain the possible suffixes for number scaling
numScaleList = ["", "K", "M", "B", "t”, “q", "Q", "s", "S", "o", "n", "d", "U", "D", "T", "Qt", "Qd", "Sd", "St", "O", "N", "v", "c"]

#scales the numbers appropriately for the wallet to look nice
def numberScaling(input):
    x = input
    amount = 0
    while x >= 1000:
        x = x / 1000
        amount += 1
    return str(round(x, 2)) + numScaleList[amount]

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
    mineArea = pygame.draw.circle(screen, Colors.black, (320, 300), 60, 60) #The click circle to generate ores
    clickValue = font.render(numberScaling(gameData.getStat("Base Click Value").getValue() * gameData.getStat("Click Multiplier").getValue()), True, Colors.white)
    screen.blit(clickValue, (320, 300))
    return mineArea

#draws in the upgrade circle
def drawUpgrade(upgrade:classes.Upgrade, x:float, y:float):
    upgradeArea = pygame.draw.rect(screen, Colors.black, (x - 30, y - 28, 200, 50)) #The click circle to generate ores
    screen.blit(font.render("Cost: " + str(numberScaling(upgrade.getRawCost())) + upgrade.getUpgradeOre(), True, Colors.white), (x-20, y))
    screen.blit(font.render(upgrade.getName(), True, Colors.white), (x-20, y-20))
    return upgradeArea

def drawNextMine():
    mine = gameData.getNextMine()
    if mine:
        nextMine = pygame.draw.circle(screen, Colors.black, (50, 350), 20, 20)
        if mine.isUnlocked():
            screen.blit(font.render("Go to " + mine.getName() + " mine", True, Colors.white), (50, 350))
        else:
            screen.blit(font.render("Unlock " + mine.getName() + " mine", True, Colors.white), (50, 350))
            screen.blit(font.render("Cost: " + numberScaling(mine.getUnlockCost()) + " coins", True, Colors.white), (50, 360))
        return nextMine


def drawPrevMine():
    mine = gameData.getPreviousMine()
    if mine:
        prevMine = pygame.draw.circle(screen, Colors.black, (50, 300), 20, 20)
    
        if mine.isUnlocked():
            screen.blit(font.render("Go to " + mine.getName() + " mine", True, Colors.white), (50, 300))
        else:
            screen.blit(font.render("Unlock " + mine.getName() + " mine", True, Colors.white), (50, 300))
            screen.blit(font.render("Cost: " + numberScaling(mine.getUnlockCost()) + " coins", True, Colors.white), (50, 310))
        return prevMine


def drawLabel(labelString:str, x:int, y:int):
    pygame.draw.rect(screen, Colors.baige, (x, y, 130, 60))
    screen.blit(font.render(labelString, True, Colors.black), (x+65/2, y+25))


#draws in the conversion circle
def drawConversion(oreName:str, x:int, y:int, color):
    #Sell 10% ore button and label
    sellTenPercent = pygame.draw.rect(screen, color, (x, y, 80, 40))
    screen.blit(font.render("Sell 10%", True, Colors.black), (x+5, y+5))
    screen.blit(font.render(oreName, True, Colors.black), (x+5, y+20))
    #Sell 50% ore button and label
    sellFiftyPercent = pygame.draw.rect(screen, color, (x+90, y, 80, 40))
    screen.blit(font.render("Sell 50%", True, Colors.black), (x+95, y+5))
    screen.blit(font.render(oreName, True, Colors.black), (x+95, y+20))
    #Sell all ore button and label
    sellAll = pygame.draw.rect(screen, color, (x+180, y, 80, 40)) #The click circle to sell ores and gain coins
    screen.blit(font.render("Sell All" , True, Colors.black), (x+185, y+5))
    screen.blit(font.render(oreName, True, Colors.black), (x+185, y+20))
    return sellTenPercent, sellFiftyPercent, sellAll

def drawMinersHeader():
    drawLabel("Miners", SCREEN_WIDTH/2 - 65, 100)
    pygame.draw.rect(screen, Colors.black, (SCREEN_WIDTH/2 - 100, 150, 25, 100))
    screen.blit((font.render("Total Miners: " + numberScaling(gameData.getStat("Total Miners").getValue()), True, Colors.black)), (SCREEN_WIDTH/2 - 95, 155))

def drawUpgradesHeader():
    drawLabel("Upgrades", (SCREEN_WIDTH * 3) / 4, 100)
    #pygame.draw.rect(screen, Colors.black, ((SCREEN_WIDTH * 3) / 4 - 165, 150, 25, 100))
    #screen.blit((font.render("Total Miners: " + numberScaling(gameData.getStat("Total Miners").getValue()), True, Colors.black)), (SCREEN_WIDTH/2 - 95, 155))


#draws in the circles to buy miners and assign miners, displays miner counts.
def drawMinerButtons(mineName:str):
    buyMiner = pygame.draw.circle(screen, Colors.red, (50, 100), 20, 20)
    screen.blit((font.render(numberScaling(gameData.getStat("Total Miners").getValue()), True, Colors.white)), (50, 100))
    screen.blit((font.render("Buy Miner", True, Colors.white)), (50-20, 100-20))
    assignMiner = pygame.draw.circle(screen, Colors.blue, (50, 150), 20, 20)
    screen.blit((font.render("Assign Miner", True, Colors.white)), (50-20, 150-20))
    screen.blit((font.render(numberScaling(gameData.getMine(mineName).getMinerCount()), True, Colors.white)), (50, 150))
    return buyMiner, assignMiner

def handleSellers(eventPos, tenSeller, fiftySeller, allSeller, oreName):
    if tenSeller.collidepoint(eventPos):
        gameData.sellOre(gameData.getOre(oreName), 0.1)
    if fiftySeller.collidepoint(eventPos):
        gameData.sellOre(gameData.getOre(oreName), 0.5)
    if allSeller.collidepoint(eventPos):
        gameData.sellOre(gameData.getOre(oreName), 1)

def handleMiners():
    pass

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
                    # if buyMiners.collidepoint(event.pos):
                    #     gameData.buyMiner()
                    # if assignMiners.collidepoint(event.pos):
                    #     gameData.assignMiners(gameData.activeMine, 1)
                    if clickBaseUpgrade.collidepoint(event.pos):
                        gameData.getUpgrade("Click_Base_Count").buyUpgrade()
                    #decreases coin amount by 10, and increases the multiplier by one (buys an incerase in a multipier for 10 coins)
                    if clickMultUpgrade.collidepoint(event.pos):
                        gameData.getUpgrade("Click_Multiplier").buyUpgrade()
                    if workSpeed.collidepoint(event.pos):
                        if gameData.getUpgrade("Miner_Speed").getCap() > 0:
                            gameData.getUpgrade("Miner_Speed").buyUpgrade()
                            gameData.getUpgrade("Miner_Speed").setCap(gameData.getUpgrade("Miner_Speed").getCap() - 1)
                    if workCost.collidepoint(event.pos):
                        if gameData.getUpgrade("Miner_Cost").getCap() > 0:
                            gameData.getUpgrade("Miner_Cost").buyUpgrade()
                            gameData.getUpgrade("Miner_Cost").setCap(gameData.getUpgrade("Miner_Cost").getCap() - 1)
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
            mineArea = drawMine()
            nextMine = drawNextMine()
            previousMine = drawPrevMine()
            swapScreenToSmith = drawButton("To Smithing", 600, 600)
            swapScreenToStats = drawButton("To Stats", 700, 600)
        if activeScreen == SMITH_SCREEN:
            screen.fill(background)
            drawWallet()
            #SELLERS
            drawLabel("Sell Ores", 95, 100)
            drawMinersHeader()
            clickBaseUpgrade = drawUpgrade(gameData.getUpgrade("Click_Base_Count"), (SCREEN_WIDTH * 3) / 4, 250)
            clickMultUpgrade = drawUpgrade(gameData.getUpgrade("Click_Multiplier"), (SCREEN_WIDTH * 3) / 4, 350)
            workSpeed = drawUpgrade(gameData.getUpgrade("Miner_Speed"), (SCREEN_WIDTH * 3) / 4, 450)
            workCost = drawUpgrade(gameData.getUpgrade("Miner_Cost"), (SCREEN_WIDTH * 3) / 4, 550)
            sellTenPercentCopper, sellFiftyPercentCopper, sellAllCopper = drawConversion("Copper", 25, 200, Colors.copper)
            sellTenPercentIron, sellFiftyPercentIron, sellAllIron = drawConversion("Iron", 25, 250, Colors.iron)
            sellTenPercentSilver, sellFiftyPercentSilver, sellAllSilver = drawConversion("Silver", 25, 300, Colors.silver)
            sellTenPercentGold, sellFiftyPercentGold, sellAllGold = drawConversion("Gold", 25, 350, Colors.gold)
            sellTenPercentDiamond, sellFiftyPercentDiamond, sellAllDiamond = drawConversion("Diamond", 25, 400, Colors.diamond)
            swapScreenToMine = drawButton("To Mine", 600, 600)
            #buyCopperMiners, assignCopperMiners = drawMiners()
            drawUpgradesHeader()
        if activeScreen == CONTRACT_SCREEN:
            pass
        if activeScreen == STAT_SCREEN:
            screen.fill(background)
            screen.blit(font.render(numberScaling(gameData.getStat("Total Clicks").getValue()), True, Colors.white), (700, 100)) #TO move
            screen.blit(font.render(numberScaling(gameData.getStat("Total Coin Earned").getValue()), True, Colors.white), (700, 200)) #TO move
            screen.blit(font.render(str(round(gameData.getStat("Time Played").getValue(), 2)), True, Colors.white), (700, 300)) #TO move
            screen.blit(font.render(numberScaling(gameData.getStat("Total Copper Earned").getValue()), True, Colors.white), (700, 400)) #TO move
            screen.blit(font.render(numberScaling(gameData.getStat("Total Iron Earned").getValue()), True, Colors.white), (900, 100)) #TO move
            screen.blit(font.render(numberScaling(gameData.getStat("Total Silver Earned").getValue()), True, Colors.white), (900, 200)) #TO move
            screen.blit(font.render(numberScaling(gameData.getStat("Total Gold Earned").getValue()), True, Colors.white), (900, 300)) #TO move
            screen.blit(font.render(numberScaling(gameData.getStat("Total Diamond Earned").getValue()), True, Colors.white), (900, 400)) #TO move
            swapScreenToMine = drawButton("To Mine", 700, 600)
        if activeScreen == RETIRE_SCREEN:
            pass


        gameData.work()

        pygame.display.flip()

pygame.quit()