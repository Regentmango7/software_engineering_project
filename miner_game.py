# CLICKER GAME

import pygame
import Colors
pygame.init()

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