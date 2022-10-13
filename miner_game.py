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

def drawMine():
    mineArea = pygame.draw.circle(screen, Colors.black, (320, 300), 60, 60) #The click circle to generate ores
    clickValue = font.render(str(orePerClick), True, Colors.white)
    totOre = font.render(str(oreAmount), True, Colors.black)
    screen.blit(clickValue, (320, 300))
    screen.blit(totOre, (10, 10))
    return mineArea

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
                oreAmount += 1
    screen.fill(background)
    mineArea = drawMine()
    pygame.display.flip()

pygame.quit()