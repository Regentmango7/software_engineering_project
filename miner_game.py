# CLICKER GAME

import pygame
import Colors
pygame.init()

# color library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
purple = (127, 0 , 255)
orange = (255, 165, 0)


def save():
    print("Game is closed")

# Main body of code
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            running = False


pygame.quit()