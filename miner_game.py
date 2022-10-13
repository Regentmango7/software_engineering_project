# MINE CLICKER GAME

import pygame
import Colors
pygame.init()

def save():
    print("Game is closed")

#create screen, background, framerate, and font
screen = pygame.display.set_mode([640, 400])
pygame.display.set_caption("Click Miners")
background = Colors.gray
framerate = 60
font = pygame.font.Font("freesansbold.ttf", 16)
timer = pygame.time.Clock()

#game variables
oreAmount = 0
orePerClick = 1
coinAmount = 0
<<<<<<< Updated upstream
multiplier = 1
=======
totalWorkers = 0
activeWorkers = 0
>>>>>>> Stashed changes

<<<<<<< Updated upstream
# Draws the wallet text box.
=======
#draws in the wallet, which contains the ore amount and coin amount
>>>>>>> Stashed changes
def drawWallet():
    wallet = pygame.draw.rect(screen, Colors.baige, (10, 10, 100, 50))
    totOre = font.render(str(oreAmount), True, Colors.black)
    totCoin = font.render(str(coinAmount), True, Colors.black)
    screen.blit(totOre, (15, 15))
    screen.blit(totCoin, (15, 30))
    return wallet

<<<<<<< Updated upstream
# Draws the mine button
=======
#draws in the mine clicking area, and displays the ores per click
>>>>>>> Stashed changes
def drawMine():
    mineArea = pygame.draw.circle(screen, Colors.black, (320, 300), 60, 60) #The click circle to generate ores
    clickValue = font.render(str(orePerClick), True, Colors.white)
    screen.blit(clickValue, (320, 300))
    return mineArea

<<<<<<< Updated upstream
# Draws the upgrade button
=======
#draws in the upgrade circle
>>>>>>> Stashed changes
def drawUpgrade():
    upgradeArea = pygame.draw.circle(screen, Colors.black, (500, 100), 20, 20) #The click circle to generate ores
    return upgradeArea

<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
#draws in the conversion circle
>>>>>>> Stashed changes
def drawConversion():
    oreToCash = pygame.draw.circle(screen, Colors.black, (500, 200), 20, 20) #The click circle to generate ores
    return oreToCash

#draws in the multiplier circle, and displays the current multiplier 
def drawMultiplier():
    clickMult = pygame.draw.circle(screen, Colors.black, (500, 300), 20, 20) #The click circle to generate ores
    multValue = font.render(str(multiplier), True, Colors.white)
    screen.blit(multValue, (500, 300))
    return clickMult
=======
def drawWorkers():
    buyWorker = pygame.draw.circle(screen, Colors.red, (50, 100), 20, 20)
    screen.blit((font.render(str(totalWorkers), True, Colors.white)), (50, 100))
    assignWorker = pygame.draw.circle(screen, Colors.blue, (100, 100), 20, 20)
    screen.blit((font.render(str(activeWorkers), True, Colors.white)), (100, 100))
    return buyWorker, assignWorker
>>>>>>> Stashed changes

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
                oreAmount += (orePerClick * multiplier)
            #increases the base ore per click
            if upgradeArea.collidepoint(event.pos):
<<<<<<< Updated upstream
                orePerClick += 1
            #converts all ore to cash at a one to one ration
            if oreToCash.collidepoint(event.pos):
                coinAmount += oreAmount
                oreAmount = 0
            #decreases coin amount by 10, and increases the multiplier by one (buys an incerase in a multipier for 10 coins)
            if clickMult.collidepoint(event.pos) and coinAmount > 9:
                coinAmount -= 10
                multiplier += 1
<<<<<<< Updated upstream
=======
                orePerClick *= 2
            if buyWorkers.collidepoint(event.pos):
                totalWorkers += 1
            if assignWorkers.collidepoint(event.pos) and activeWorkers < totalWorkers:
                activeWorkers += 1
>>>>>>> Stashed changes

=======
    
    #draws a series of objects
>>>>>>> Stashed changes
    screen.fill(background)
    buyWorkers, assignWorkers = drawWorkers()
    wallet = drawWallet()
    mineArea = drawMine()
    oreToCash = drawConversion()  
    upgradeArea = drawUpgrade()
    clickMult = drawMultiplier()
    pygame.display.flip()

pygame.quit()