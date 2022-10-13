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

def drawCircle():
    pygame.draw.circle(screen, Colors.black, (320, 300), 60, 60)

# Main body of code
running = True
while running:
    timer.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            running = False
    screen.fill(background)
    drawCircle()
    pygame.display.flip()

pygame.quit()