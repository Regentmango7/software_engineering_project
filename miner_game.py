# MINE CLICKER GAME

from msilib.schema import Upgrade
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
oreAmount = 0
orePerClick = 1
multiplier = 1
totalWorkers = 0
activeWorkers = 0
workerTime = 0
benchmark = 0
store = 0
firstRun = False


#sells ratio * ore.amount for coins
# 1 <= ratio < 0
def sellOre(ore=classes.OreType, ratio=float):
    oreLeft = ore.getAmount() * (1-ratio)
    oreSold = ore.getAmount() * ratio
    ore.setAmount(oreLeft)
    gameData.coin.addOre(oreSold * ore.getValue())
        

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

def mineAction(isMiner=False):
    ore = []
    probability = []
    for rate in gameData.activeMine.getOreRates():
        ore.append(rate.getOre())
        probability.append(rate.getRate())
    obtainedOre = choice(ore, p=probability)
    if isMiner:
        obtainedOre.amount += gameData.minerValMulti.getValue() * gameData.activeMine.getMinerCount()
    else: 
        obtainedOre.amount += gameData.clickBaseValue.getValue() * gameData.clickMulti.getValue()

def buyWorker():
    cost = pow(10, gameData.minersTotal.getValue() + 1)
    if gameData.coin.getAmount() >= cost:
        gameData.minersTotal.value += 1
        gameData.minersAvailable.value += 1
        gameData.coin.addOre(-cost)

def assignMiner():
    if gameData.minersAvailable.getValue() > 0:
        gameData.activeMine.assignMiner()
        gameData.minersAvailable.value -= 1

#draws in the upgrade circle
def drawBaseUpgrade(upgrade=classes.Upgrade):
    upgradeArea = pygame.draw.circle(screen, Colors.black, (500, 100), 20, 20) #The click circle to generate ores
    upgradeValue = font.render(str(upgrade.getCostString()), True, Colors.white)
    screen.blit(upgradeValue, (500, 100))
    return upgradeArea


#draws in the conversion circle
def drawConversion():
    oreToCash = pygame.draw.circle(screen, Colors.black, (500, 200), 20, 20) #The click circle to generate ores
    return oreToCash

#draws in the multiplier circle, and displays the current multiplier 
def drawMultiplierUpgrade(upgrade=classes.Upgrade):
    clickMult = pygame.draw.circle(screen, Colors.black, (500, 300), 20, 20) #The click circle to generate ores
    multValue = font.render(str(upgrade.getCostString()), True, Colors.white)
    screen.blit(multValue, (500, 300))
    return clickMult

#draws in the circles to buy workers and assign workers, displays worker counts.
def drawWorkers():
    buyWorker = pygame.draw.circle(screen, Colors.red, (50, 100), 20, 20)
    screen.blit((font.render(str(gameData.minersTotal.getValue()), True, Colors.white)), (50, 100))
    assignWorker = pygame.draw.circle(screen, Colors.blue, (100, 100), 20, 20)
    screen.blit((font.render(str(gameData.activeMine.getMinerCount()), True, Colors.white)), (100, 100))
    return buyWorker, assignWorker

#makes the workers work
def work(store, benchmark, firstRun):
    #workTimer = gameData.getMine("Copper").getWorkerTimer()
    if firstRun == False:
        store = 0
        benchmark = store
        firstRun = True
    else:
        if store >= (100):
            mineAction(True)
            firstRun = False
    store += 1
    return store, benchmark, firstRun


def save():
    print("Game is closed")

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
                assignMiner()
    if gameData.activeMine.getMinerCount() > 0:
        store, benchmark, firstRun = work(store, benchmark, firstRun)

    #draws a series of objects
    screen.fill(background)
    buyWorkers, assignWorkers = drawWorkers()
    wallet = drawWallet()
    mineArea = drawMine()
    oreToCash = drawConversion()  
    clickBaseUpgrade = drawBaseUpgrade(gameData.getUpgrade("Click_Base_Count"))
    clickMultUpgrade = drawMultiplierUpgrade(gameData.getUpgrade("Click_Multiplier"))

    pygame.display.flip()

pygame.quit()