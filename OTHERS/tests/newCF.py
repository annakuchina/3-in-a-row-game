import numpy as np
import pygame
from pygame.locals import *
import random
import sys
import math

# Define fps
clock = pygame.time.Clock()
fps = 60

class newItem(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__()
        self.image = pygame.image.load("picture_path")
        self.rect = self.image.get_rect()

pygame.init()
clock = pygame.time.Clock()

ROW_COUNT = 8
COLUMN_COUNT = 8 

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 128, 2)
BLUE = (0, 0, 255)


# newRectangle = 

itemColors = [
    RED,
    YELLOW,
    ORANGE,
    PURPLE,
    GREEN,
    BLUE
]

rectangle_draging = False

colorLen = len(itemColors)

itemArray = []


def create_board():
    board = board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board
    # Create a board


def place_piece(board, row, col, piece):
    board[row][col] = piece

rectangle = pygame.rect.Rect(176, 134, 17, 17)


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            chosenColor = random.randint(0, colorLen-1)
            pygame.draw.rect(screen, itemColors[chosenColor], (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            itemArray.append(chosenColor)
            rectangle = pygame.rect.Rect(c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)
            

                # random.randrage(1, )
                
                # pygame.draw.circle(screen, )

# def print_board(board):
#     pass

# Starting game
board = create_board()
# print_board(board)
game_over = False
turn = 0

# Load image



SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 3")
draw_board(board)
pygame.display.update()


myFont = pygame.font.SysFont("monospace", 60)


# New image
orangeItem = newItem(7, 2, "orange.png")


while not game_over:
    clock.tick(fps)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y   
    


    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()