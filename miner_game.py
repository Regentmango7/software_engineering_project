# MINE CLICKER GAME
import pygame
import Colors
import classes
pygame.init()

screenWidth = 1280
screenHeight = 720
#create screen, background, framerate, and font
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Click Miners")
background = Colors.gray
framerate = 60
font = pygame.font.Font("freesansbold.ttf", 16)
timer = pygame.time.Clock()

gameData = classes.Data()

#flags for which screen we are on
mine_screen = False
smith_screen = True
town_screen = False
retire_screen = False
stat_screen = False

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
    return x, amount

#draws in the wallet, which contains the ore amount and coin amount
def drawWallet():
    pygame.draw.rect(screen, Colors.baige, (10, 10, 300, 55))
    coinHold, coinAppend = numberScaling(round(gameData.coin.amount, 2))
    totCoin = font.render("Coins: " + str(round(coinHold, 2)) + numScaleList[coinAppend], True, Colors.black)
    screen.blit(totCoin, (15, 15))    
    copperHold, copperAppend = numberScaling(round(gameData.getOre("Copper").amount, 2))
    totCopper = font.render("Copper: " + str(round(copperHold, 2)) + numScaleList[copperAppend], True, Colors.black)
    screen.blit(totCopper, (15, 30))
    ironHold, ironAppend = numberScaling(round(gameData.getOre("Iron").amount, 2))
    totIron = font.render("Iron: " + str(round(ironHold, 2)) + numScaleList[ironAppend], True, Colors.black)
    screen.blit(totIron, (15, 45))
    silverHold, silverAppend = numberScaling(round(gameData.getOre("Silver").amount, 2))
    totSilver = font.render("Silver: " + str(round(silverHold, 2)) + numScaleList[silverAppend], True, Colors.black)
    screen.blit(totSilver, (150, 15))
    goldHold, goldAppend = numberScaling(round(gameData.getOre("Gold").amount, 2))
    totGold = font.render("Gold: " + str(round(goldHold, 2)) + numScaleList[goldAppend], True, Colors.black)
    screen.blit(totGold, (150, 30))
    diamondHold, diamondAppend = numberScaling(round(gameData.getOre("Diamond").amount, 2))
    totDiamond = font.render("Diamond: " + str(round(diamondHold, 2)) + numScaleList[diamondAppend], True, Colors.black)
    screen.blit(totDiamond, (150, 45))

#draws in the mine clicking area, and displays the ores per click
def drawMine():
    mineArea = pygame.draw.circle(screen, Colors.black, (320, 300), 60, 60) #The click circle to generate ores
    clickValue = font.render(str(gameData.clickBaseValue.getValue() * gameData.clickMulti.getValue()), True, Colors.white)
    screen.blit(clickValue, (320, 300))
    return mineArea

# if the player has x or more miners assigned to the mine, remove them from the mine and add x to minersAvailable
# if the player has less than x miners assigned, will remove all active miners from mine and add that number to minersAvailable
def unassignMiners(mine:classes.MineType, x:int):
    if mine.getMinerCount() <= x:
        mine.unassignMiners(x)
        gameData.minersAvailable.value += x
    else:
        mine.unassignMiners(mine.getMinerCount())
        gameData.minersAvailable.value += mine.getMinerCount()

#draws in the upgrade circle
def drawUpgrade(upgrade:classes.Upgrade, x:float, y:float):
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
def drawConversion(oreName:str, x:int, y:int):
    #Sell 10% ore button and label
    sellTenPercent = pygame.draw.circle(screen, Colors.black, (x, y), 20, 20)
    screen.blit(font.render("Sell 10%", True, Colors.white), (x-20, y-20))
    screen.blit(font.render(oreName, True, Colors.white), (x-20, y-5))
    #Sell 50% ore button and label
    sellFiftyPercent = pygame.draw.circle(screen, Colors.black, (x + 50, y), 20, 20)
    screen.blit(font.render("Sell 50%", True, Colors.white), (x+30, y-20))
    screen.blit(font.render(oreName, True, Colors.white), (x+30, y-5))
    #Sell all ore button and label
    sellAll = pygame.draw.circle(screen, Colors.black, (x+100, y), 20, 20) #The click circle to sell ores and gain coins
    screen.blit(font.render("Sell All" , True, Colors.white), (x+80, y-20))
    screen.blit(font.render(oreName, True, Colors.white), (x+80, y-5))
    return sellTenPercent, sellFiftyPercent, sellAll

#draws in the circles to buy workers and assign workers, displays worker counts.
def drawWorkers():
    buyWorker = pygame.draw.circle(screen, Colors.red, (50, 100), 20, 20)
    screen.blit((font.render(str(gameData.minersTotal.getValue()), True, Colors.white)), (50, 100))
    screen.blit((font.render("Buy Worker", True, Colors.white)), (50-20, 100-20))
    assignWorker = pygame.draw.circle(screen, Colors.blue, (50, 150), 20, 20)
    screen.blit((font.render("Assign Worker", True, Colors.white)), (50-20, 150-20))
    screen.blit((font.render(str(gameData.activeMine.getMinerCount()), True, Colors.white)), (50, 150))
    return buyWorker, assignWorker


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
            if mine_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #gives the player ore based on the ore per click amount multiplied by the multiplier
                    if mineArea.collidepoint(event.pos):
                        gameData.mineAction(gameData.activeMine)
                    #increases the base ore per click
                    if clickBaseUpgrade.collidepoint(event.pos):
                        gameData.getUpgrade("Click_Base_Count").buyUpgrade()
                    #decreases coin amount by 10, and increases the multiplier by one (buys an incerase in a multipier for 10 coins)
                    if clickMultUpgrade.collidepoint(event.pos):
                        gameData.getUpgrade("Click_Multiplier").buyUpgrade()
                    if buyWorkers.collidepoint(event.pos):
                        gameData.buyWorker()
                    if assignWorkers.collidepoint(event.pos):
                        gameData.assignMiners(gameData.activeMine, 1)
                    if previousMine.collidepoint(event.pos):
                        gameData.setPreviousMine()
                    if nextMine.collidepoint(event.pos):
                        gameData.setNextMine()
                    if workSpeed.collidepoint(event.pos):
                        if gameData.getUpgrade("Worker_Speed").getCap() > 0:
                            gameData.getUpgrade("Worker_Speed").buyUpgrade()
                            gameData.getUpgrade("Worker_Speed").setCap(gameData.getUpgrade("Worker_Speed").getCap() - 1)
            if smith_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sellTenPercentCopper.collidepoint(event.pos):
                        gameData.sellOre(gameData.getOre("Copper"), 0.1)
                    if sellFiftyPercentCopper.collidepoint(event.pos):
                        gameData.sellOre(gameData.getOre("Copper"), 0.5)
                    if sellAllCopper.collidepoint(event.pos):
                        gameData.sellOre(gameData.getOre("Copper"), 1)

        # OUTSIDE EVENT LOOP
        if mine_screen:
            #draws a series of objects
            screen.fill(background)
            buyWorkers, assignWorkers = drawWorkers()
            wallet = drawWallet()
            mineNameplate = drawMineName()
            mineArea = drawMine()
            nextMine = drawNextMine()
            previousMine = drawPrevMine()
            clickBaseUpgrade = drawUpgrade(gameData.getUpgrade("Click_Base_Count"), 500, 100)
            clickMultUpgrade = drawUpgrade(gameData.getUpgrade("Click_Multiplier"), 500, 300)
            workSpeed =  drawUpgrade(gameData.getUpgrade("Worker_Speed"), 400, 200)
        if smith_screen:
            screen.fill(background)
            wallet = drawWallet()
            sellTenPercentCopper, sellFiftyPercentCopper, sellAllCopper = drawConversion("Copper", 30, 110)
            #buyCopperWorkers, assignCopperWorkers = drawWorkers()
        if town_screen:
            pass
        if stat_screen:
            pass
        if retire_screen:
            pass


        gameData.work()

        pygame.display.flip()

pygame.quit()