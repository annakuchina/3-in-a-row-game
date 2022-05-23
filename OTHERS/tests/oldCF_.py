from os import system
import numpy as np
import pygame
import random
import sys
import math

ROW_COUNT = 8
COLUMN_COUNT = 8 

FPS = 30
clock = pygame.time.Clock()

# Load all images


RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 128, 2)
BLUE = (0, 0, 255)

class Key(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, id):
        super(Key, self).__init__()
        
        self.i



class Item(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.width = 100
        self.height = 100
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

# see where mouse is
# if the user is dragging,
# get their mouse position in x and y -> round them up/down to nearest square
# - dont work if in between squares
# smooth drag in between - movement

# if it is allowed, switch the positions. if not, don't
# - need to record a record of the different objects and grid to check with internal system


itemColors = [
    RED,
    YELLOW,
    ORANGE,
    PURPLE,
    GREEN,
    BLUE
]

#later, make these images instead of just colors

rectangle_draging = False

colorLen = len(itemColors)

itemArray = []


def create_board():
    board = board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board
    # Create a board


def place_piece(board, row, col, piece):
    board[row][col] = piece

# rectangle = pygame.rect.Rect(176, 134, 17, 17)

itemDictionary= {}

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            chosenColor = itemColors[random.randint(0, colorLen-1)]
            pygame.draw.rect(screen, chosenColor, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            rectangle = pygame.rect.Rect(c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)
            itemDictionary[chosenColor] = [c, rectangle]
            print(chosenColor)
            # print(rectangle)
            # print("hi")


# def print_board(board):
#     pass


# Starting game
board = create_board()
# print_board(board)
game_over = False
turn = 0


pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 60)

print(itemDictionary)
print("zzz")

while not game_over:
    # event.button 1 -> left click
    # event.button 2 -> right click
    #event.button 3 -> middle click

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("hi")
            if event.button == 1:
                print("hhh")
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


    clock.tick(FPS)

pygame.quit()
