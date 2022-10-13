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

def drawWallet():
    wallet = pygame.draw.rect(screen, Colors.baige, (10, 10, 100, 50))
    totOre = font.render(str(oreAmount), True, Colors.black)
    totCoin = font.render(str(coinAmount), True, Colors.black)
    screen.blit(totOre, (15, 15))
    screen.blit(totCoin, (15, 30))
    return wallet

def drawMine():
    mineArea = pygame.draw.circle(screen, Colors.black, (320, 300), 60, 60) #The click circle to generate ores
    clickValue = font.render(str(orePerClick), True, Colors.white)
    screen.blit(clickValue, (320, 300))
    return mineArea

def drawUpgrade():
    upgradeArea = pygame.draw.circle(screen, Colors.black, (500, 100), 20, 20) #The click circle to generate ores
    return upgradeArea

def drawConversion():
    oreToCash = pygame.draw.circle(screen, Colors.black, (500, 200), 20, 20) #The click circle to generate ores
    return oreToCash

# Main body of code
running = True
while running:
    timer.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mineArea.collidepoint(event.pos):
                oreAmount += orePerClick
            if upgradeArea.collidepoint(event.pos):
                orePerClick += 1
            if oreToCash.collidepoint(event.pos):
                coinAmount += oreAmount
                oreAmount = 0
    screen.fill(background)
    wallet = drawWallet()
    mineArea = drawMine()
    oreToCash = drawConversion()  
    upgradeArea = drawUpgrade()
    pygame.display.flip()

pygame.quit()