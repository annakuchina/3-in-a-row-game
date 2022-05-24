import pygame
from pygame.locals import *
import os
import sys
import itertools

SCREEN = pygame.display.set_mode((800, 800))
ROW_COUNT = 8
COLUMN_COUNT = 8

# MUSHROOM_SPRITE = pygame.image.load(os.path.join("images", "mushroom.png")).convert_alpha()
# POTION_SPRITE = pygame.image.load(os.path.join("sprites", "potion.png")).convert_alpha()

# BLUE_SPRITE = pygame.image.load(os.path.join("images", "blue.png")).convert_alpha()
# ORANGE_SPRITE = pygame.image.load(os.path.join("images", "orange.png")).convert_alpha()
# PURPLE_SPRITE = pygame.image.load(os.path.join("images", "purple.png")).convert_alpha()
# YELLOW_SPRITE = pygame.image.load(os.path.join("images", "yellow.png")).convert_alpha()


# itemTypes = [
#     "mushroom",
#     "potion",
#     "blue",
#     "orange",
#     "purple",
#     "yellow"
# ]

itemTypes = [
    "red",
    "green",
    "blue",
    "orange",
    "purple",
    "yellow"
]

#do the loading inside of the game maybe, or convert.alpha
deleteOrange = ["orange", "orange-small", "orange-smaller", "white"]

# deleteOrange = [os.path.join("images", "orange.png")).convert_alpha(), pygame.image.load(os.path.join("images", "orange-small.png")).convert_alpha(), pygame.image.load(os.path.join("images", "orange-smaller.png")).convert_alpha()]