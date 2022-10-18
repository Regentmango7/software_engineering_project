# MINE CLICKER GAME

from re import X
from numpy.random import choice
import pygame
import Colors
import classes
pygame.init()


#create screen, background, framerate, and font
screen = pygame.display.set_mode([640, 400])
pygame.display.set_caption("Click Miners")
background = Colors.gray
framerate = 60
font = pygame.font.Font("freesansbold.ttf", 16)
timer = pygame.time.Clock()

gameData = classes.Data()

#game variables
store = 0
firstRun = False


#sells ratio * ore.amount for coins
# 1 <= ratio < 0
def sellOre(ore=classes.OreType, ratio=float):
    oreLeft = ore.getAmount() * (1-ratio)
    oreSold = ore.getAmount() * ratio
    ore.setAmount(oreLeft)
    gameData.coin.addOre(oreSold * ore.getValue())

#if there is one, set activeMine to the mine after the current activeMine
def setNextMine():
    index = gameData.MINE_ORDER.index(gameData.activeMine.getName())+1
    if not index >= len(gameData.MINE_ORDER):
        gameData.activeMine = gameData.getMine(gameData.MINE_ORDER[index])

#if there is one, set activeMine to the mine before the current activeMine.
def setPreviousMine():
    index = gameData.MINE_ORDER.index(gameData.activeMine.getName())-1
    if not index < 0:
        gameData.activeMine = gameData.getMine(gameData.MINE_ORDER[index])

#draws in the wallet, which contains the ore amount and coin amount
def drawWallet():
    wallet = pygame.draw.rect(screen, Colors.baige, (10, 10, 125, 55))
    totCoin = font.render("Coins: " + str(round(gameData.coin.amount, 2)), True, Colors.black)
    screen.blit(totCoin, (15, 15))    
    totOre = font.render("Copper: " + str(round(gameData.getOre("Copper").amount, 2)), True, Colors.black)
    screen.blit(totOre, (15, 30))
    totIron = font.render("Iron: " + str(round(gameData.getOre("Iron").amount, 2)), True, Colors.black)
    screen.blit(totIron, (15, 45))
    return wallet

#draws in the mine clicking area, and displays the ores per click
def drawMine():
    mineArea = pygame.draw.circle(screen, Colors.black, (320, 300), 60, 60) #The click circle to generate ores
    clickValue = font.render(str(gameData.clickBaseValue.getValue() * gameData.clickMulti.getValue()), True, Colors.white)
    screen.blit(clickValue, (320, 300))
    return mineArea

#
def mineAction(isMiner=False, mine=gameData.activeMine):
    ore = []
    probability = []
    for rate in mine.getOreRates():
        ore.append(rate.getOre())
        probability.append(rate.getRate())
    obtainedOre = choice(ore, p=probability)
    if isMiner:
        obtainedOre.amount += gameData.minerValMulti.getValue() * gameData.activeMine.getMinerCount()
    else: 
        obtainedOre.amount += gameData.clickBaseValue.getValue() * gameData.clickMulti.getValue()

#if the player has enough coins, buy the next worker
def buyWorker():
    cost = pow(10, gameData.minersTotal.getValue() + 1)
    if gameData.coin.getAmount() >= cost:
        gameData.minersTotal.value += 1
        gameData.minersAvailable.value += 1
        gameData.coin.addOre(-cost)

#if the player has enough miners available, assign x miners to the mine given.
def assignMiners(mine=classes.MineType, x=int):
    if gameData.minersAvailable.getValue() >= x:
        mine.assignMiners(x)
        gameData.minersAvailable.value -= x

# if the player has x or more miners assigned to the mine, remove them from the mine and add x to minersAvailable
# if the player has less than x miners assigned, will remove all active miners from mine and add that number to minersAvailable
def unassignMiners(mine=classes.MineType, x=int):
    if mine.getMinerCount() <= x:
        mine.unassignMiners(x)
        gameData.minersAvailable.value += x
    else:
        mine.unassignMiners(mine.getMinerCount())
        gameData.minersAvailable.value += mine.getMinerCount()

#draws in the upgrade circle
def drawUpgrade(upgrade=classes.Upgrade, x=float, y=float):
    upgradeArea = pygame.draw.circle(screen, Colors.black, (x, y), 20, 20) #The click circle to generate ores
    screen.blit(font.render(str(upgrade.getCostString()), True, Colors.white), (x-20, y))
    screen.blit(font.render(upgrade.getName(), True, Colors.white), (x-20, y-20))
    return upgradeArea

def drawMineName():
    mineNameplate = pygame.draw.rect(screen, Colors.baige, (320-65, 50, 130, 60))
    screen.blit(font.render(gameData.activeMine.getName(), True, Colors.black), (325-65, 65))
    return mineNameplate

def drawNextMine():
    nextMine = pygame.draw.circle(screen, Colors.black, (50, 300), 20, 20)
    screen.blit(font.render("Next Mine", True, Colors.white), (50, 300))
    return nextMine

def drawPrevMine():
    prevMine = pygame.draw.circle(screen, Colors.black, (50, 250), 20, 20)
    screen.blit(font.render("Previous Mine", True, Colors.white), (50, 250))
    return prevMine


#draws in the conversion circle
def drawConversion():
    oreToCash = pygame.draw.circle(screen, Colors.black, (500, 200), 20, 20) #The click circle to generate ores
    screen.blit(font.render("Sell All Copper", True, Colors.white), (500-20, 200-20))
    return oreToCash

#draws in the circles to buy workers and assign workers, displays worker counts.
def drawWorkers():
    buyWorker = pygame.draw.circle(screen, Colors.red, (50, 100), 20, 20)
    screen.blit((font.render(str(gameData.minersTotal.getValue()), True, Colors.white)), (50, 100))
    screen.blit((font.render("Buy Worker", True, Colors.white)), (50-20, 100-20))
    assignWorker = pygame.draw.circle(screen, Colors.blue, (50, 150), 20, 20)
    screen.blit((font.render("Assign Worker", True, Colors.white)), (50-20, 150-20))
    screen.blit((font.render(str(gameData.activeMine.getMinerCount()), True, Colors.white)), (50, 150))
    return buyWorker, assignWorker

#makes the workers work
def work(store, firstRun):
    if store >= (100):
        mineAction(True)
        firstRun = False
        store = 0
    store += 1
    return store, firstRun


def save():
    print("Game is closed")


if __name__ == "__main__":
    # Main body of code
    running = True
    while running:
        timer.tick(framerate)
        for event in pygame.event.get():
            #quits the game
            if event.type == pygame.QUIT:
                save()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #gives the player ore based on the ore per click amount multiplied by the multiplier
                if mineArea.collidepoint(event.pos):
                    mineAction()
                #increases the base ore per click
                if clickBaseUpgrade.collidepoint(event.pos):
                    gameData.getUpgrade("Click_Base_Count").buyUpgrade()
                #converts all ore to cash at a one to one ration
                if oreToCash.collidepoint(event.pos):
                    sellOre(gameData.getOre("Copper"), 1)
                #decreases coin amount by 10, and increases the multiplier by one (buys an incerase in a multipier for 10 coins)
                if clickMultUpgrade.collidepoint(event.pos):
                    gameData.getUpgrade("Click_Multiplier").buyUpgrade()
                if buyWorkers.collidepoint(event.pos):
                    buyWorker()
                if assignWorkers.collidepoint(event.pos):
                    assignMiners(gameData.activeMine, 1)
                if previousMine.collidepoint(event.pos):
                    setPreviousMine()
                if nextMine.collidepoint(event.pos):
                    setNextMine()
        if gameData.activeMine.getMinerCount() > 0:
            store, firstRun = work(store, firstRun)

        #draws a series of objects
        screen.fill(background)
        buyWorkers, assignWorkers = drawWorkers()
        wallet = drawWallet()
        mineNameplate = drawMineName()
        mineArea = drawMine()
        oreToCash = drawConversion()
        nextMine = drawNextMine()
        previousMine = drawPrevMine()  
        clickBaseUpgrade = drawUpgrade(gameData.getUpgrade("Click_Base_Count"), 500, 100)
        clickMultUpgrade = drawUpgrade(gameData.getUpgrade("Click_Multiplier"), 500, 300)

        pygame.display.flip()

pygame.quit()