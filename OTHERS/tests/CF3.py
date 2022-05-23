# import numpy as np
import pygame
import random
import sys
import math
import os
from pathlib import Path

class gameObject(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        #Takes an image, draws a rectangle around the image


# General setup
pygame.init()
clock = pygame.time.Clock()

# Game screen
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# background = pygame.image.load(os.path.join("./images", "orange.png"))

# RED = (247, 111, 111)
# BLUE = (111, 156, 247)
# GREEN = (144, 249, 132)
# ORANGE = (255, 158, 94)
# PURPLE = (188, 137, 255)
# YELLOW = (255, 245, 140)

# testObj = 



BLUE = pygame.image.load(os.path.join("images", "blue.png"))
GREEN = pygame.image.load(os.path.join("images", "green.png"))
ORANGE = pygame.image.load(os.path.join("images", "orange.png"))
PURPLE = pygame.image.load(os.path.join("images", "purple.png"))
RED = pygame.image.load(os.path.join("images", "red.png"))
YELLOW = pygame.image.load(os.path.join("images", "yellow.png"))

gameObject = gameObject(50, 50, 100, 100, (255, 255, 255))

gameObject_group = pygame.sprite.Group()
gameObject_group.add(gameObject)


rectangle = pygame.rect.Rect(176, 134, 17, 17)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw whatever frame was painted
    pygame.display.flip()
    # screen.blit(background, (0, 0))
    
    # gameObject_group.draw(screen)


    clock.tick(60)