import pygame
from pygame.locals import *
import os
import sys
import itertools

SCREEN = pygame.display.set_mode((800, 800))

MUSHROOM_SPRITE = pygame.image.load(os.path.join("sprites", "mushroom.png")).convert_alpha()
POTION_SPRITE = pygame.image.load(os.path.join("sprites", "potion.png")).convert_alpha()

BLUE = pygame.image.load(os.path.join("images", "blue.png")).convert_alpha()
ORANGE = pygame.image.load(os.path.join("images", "orange.png")).convert_alpha()
PURPLE = pygame.image.load(os.path.join("images", "purple.png")).convert_alpha()
YELLOW = pygame.image.load(os.path.join("images", "yellow.png")).convert_alpha()