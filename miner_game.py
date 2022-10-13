# CLICKER GAME

import pygame
import Colors
pygame.init()

def save():
    print("Game is closed")

screen = pygame.display.set_mode([640, 400])
pygame.display.set_caption("Click Miners")
background = Colors.black
framerate = 60
font = pygame.font.Font("freesansbold.ttf", 16)
timer = pygame.time.Clock()

# Main body of code
running = True
while running:
    timer.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            running = False
    screen.fill(background)

    pygame.display.flip()

pygame.quit()