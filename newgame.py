from operator import ne
from optparse import Values
import os, pygame, random, sys, math
from unicodedata import name
import numpy as np
from os import system
import time
import globs
from gameFunctions import itemCollect, checkBoard, deleteItems

# myFont = pygame.font.SysFont("monospace", 60)


FPS = 60
clock = pygame.time.Clock()
pygame.init()

globs.SCREEN.fill((255, 255, 255))

itemTypes = globs.itemTypes

# Load all images

# itemTypes = [
#     "red",
#     "yellow",
#     "orange",
#     "purple",
#     "green",
#     "blue"
# ]


SQUARESIZE = 10
width = globs.COLUMN_COUNT * SQUARESIZE
height = (globs.ROW_COUNT+1) * SQUARESIZE

size = (width, height)

board = {}


left = 0
right = 0
up = 0
down = 0

#-----------------
#SAMPLE BOARDS

# VERTICAL 3 in a row
# board = {0: ['purple', 'yellow', 'yellow', 'blue', 'orange', 'green', 'green', 'blue'], 1: ['purple', 'blue', 'yellow', 'blue', 'yellow', 'purple', 'orange', 'orange'], 2: ['yellow', 'orange', 'blue', 'green', 'orange', 'orange', 'red', 'green'], 3: ['blue', 'orange', 'green', 'blue', 'blue', 'green', 'green', 'yellow'], 4: ['blue', 'green', 'blue', 'orange', 'red', 'purple', 'purple', 'yellow'], 5: ['orange', 'yellow', 'orange', 'yellow', 'blue', 'yellow', 'orange', 'yellow'], 6: ['yellow', 'red', 'purple', 'purple', 'yellow', 'red', 'red', 'orange'], 7: ['yellow', 'red', 'blue', 'yellow', 'purple', 'blue', 'orange', 'blue']}
#Only 1
# board = {0: ['red', 'red', 'orange', 'green', 'yellow', 'purple', 'purple', 'blue'], 1: ['red', 'yellow', 'red', 'yellow', 'yellow', 'orange', 'green', 'blue'], 2: ['orange', 'red', 'red', 'yellow', 'green', 'orange', 'orange', 'red'], 3: ['red', 'red', 'orange', 'green', 'red', 'orange', 'red', 'yellow'], 4: ['yellow', 'yellow', 'blue', 'green', 'red', 'green', 'green', 'orange'], 5: ['orange', 'red', 'orange', 'yellow', 'orange', 'blue', 'orange', 'orange'], 6: ['blue', 'blue', 'orange', 'orange', 'blue', 'green', 'green', 'yellow'], 7: ['purple', 'yellow', 'yellow', 'orange', 'blue', 'red', 'yellow', 'green']}

# VERTICAL 4 in a row
# board = {0: ['blue', 'yellow', 'purple', 'purple', 'green', 'red', 'green', 'purple'], 1: ['blue', 'red', 'green', 'green', 'blue', 'orange', 'orange', 'orange'], 2: ['green', 'blue', 'red', 'orange', 'green', 'green', 'red', 'red'], 3: ['green', 'purple', 'purple', 'orange', 'red', 'blue', 'red', 'yellow'], 4: ['orange', 'purple', 'orange', 'blue', 'red', 'yellow', 'blue', 'blue'], 5: ['green', 'orange', 'purple', 'blue', 'red', 'blue', 'yellow', 'green'], 6: ['green', 'green', 'purple', 'orange', 'red', 'purple', 'yellow', 'orange'], 7: ['orange', 'green', 'red', 'blue', 'orange', 'yellow', 'blue', 'blue']}

# HORIZONTAL 3 in a row
# board = {0: ['purple', 'purple', 'purple', 'yellow', 'purple', 'red', 'purple', 'blue'], 1: ['yellow', 'blue', 'red', 'orange', 'blue', 'purple', 'green', 'green'], 2: ['yellow', 'red', 'yellow', 'orange', 'green', 'red', 'purple', 'green'], 3: ['red', 'blue', 'red', 'green', 'blue', 'blue', 'purple', 'blue'], 4: ['green', 'yellow', 'orange', 'orange', 'red', 'blue', 'green', 'yellow'], 5: ['green', 'blue', 'purple', 'green', 'green', 'green', 'blue', 'green'], 6: ['blue', 'blue', 'red', 'red', 'blue', 'blue', 'purple', 'green'], 7: ['purple', 'yellow', 'yellow', 'blue', 'red', 'yellow', 'yellow', 'blue']}

# 2 HORIZONTAL 4 in a row
# board = {0: ['purple', 'purple', 'green', 'yellow', 'green', 'purple', 'red', 'yellow'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'blue', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'orange', 'blue'], 3: ['green', 'red', 'purple', 'red', 'red', 'red', 'red', 'red'], 4: ['blue', 'blue', 'red', 'green', 'purple', 'blue', 'purple', 'orange'], 5: ['purple', 'green', 'green', 'yellow', 'blue', 'purple', 'green', 'green'], 6: ['yellow', 'green', 'green', 'green', 'green', 'purple', 'orange', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# board = {0: ['purple', 'purple', 'purple', 'yellow', 'green', 'purple', 'purple', 'purple'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'purple', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'purple', 'blue'], 3: ['green', 'red', 'purple', 'red', 'red', 'red', 'purple', 'red'], 4: ['blue', 'green', 'red', 'green', 'purple', 'blue', 'green', 'orange'], 5: ['green', 'green', 'green', 'blue', 'green', 'blue', 'purple', 'green'], 6: ['yellow', 'green', 'green', 'purple', 'green', 'purple', 'purple', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# board = {0: ['purple', 'purple', 'purple', 'yellow', 'green', 'purple', 'purple', 'purple'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'purple', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'purple', 'blue'], 3: ['green', 'red', 'purple', 'red', 'blue', 'red', 'purple', 'red'], 4: ['blue', 'green', 'red', 'green', 'purple', 'blue', 'green', 'orange'], 5: ['green', 'red', 'green', 'blue', 'green', 'blue', 'purple', 'green'], 6: ['yellow', 'green', 'green', 'purple', 'green', 'purple', 'blue', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# MULTIPLES
# board = {0: ['green', 'green', 'purple', 'green', 'yellow', 'yellow', 'purple', 'red'], 1: ['green', 'yellow', 'green', 'green', 'yellow', 'blue', 'blue', 'orange'], 2: ['green', 'red', 'yellow', 'purple', 'green', 'orange', 'yellow', 'blue'], 3: ['blue', 'blue', 'blue', 'purple', 'green', 'green', 'blue', 'green'], 4: ['purple', 'purple', 'red', 'yellow', 'yellow', 'green', 'green', 'blue'], 5: ['purple', 'blue', 'yellow', 'red', 'purple', 'blue', 'red', 'yellow'], 6: ['red', 'purple', 'yellow', 'blue', 'blue', 'green', 'yellow', 'purple'], 7: ['orange', 'red', 'yellow', 'green', 'blue', 'blue', 'yellow', 'red']}

#END SAMPLE BOARDS
#-----------------

class Key(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, id):
        super(Key, self).__init__()
        self.i

rectangle_draging = False
itemLen = len(itemTypes)
itemArray = []

rectangle = pygame.rect.Rect(176, 134, 17, 17)

image = ""

class Item(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos, itemSize):
        super().__init__()

        # com
        completeImgPath = os.path.join("images", (str(picture_path) + ".png"))
        # add checking here later

        # print(picture_path)
        # print(pos)
        # print("   hi")

        self.image = pygame.image.load(completeImgPath)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]  #put x coord here
        self.rect.y = pos[1] # put y coord here
        self.width = itemSize
        self.height = itemSize
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        # the picture, and the rectangle around the picture

        # animateRemove(board[currentRow][colSplitCount])

    #     def animateMoveDown(item):
    #         pygame.time.get_ticks(60)
    #         iterations = 60
            
    #         self.rect.y -= 1
    #         board[currentRow][colSplitCount]
    #         pass
            


    # def removeItem():
    #     globs.SCREEN.blit(self.image, (self.x - 16, self.y - 11))
    
    # def moveDownItem(self, picture_path, pos, itemSize):
    #     pass


itemGroup = pygame.sprite.Group()
itemSize = 80
innerSpacing = 5
outerTopMargin = 100
outerLeftMargin = 60

itemCount = 0


def makeBoard(board):
    r = 0
    for r, columnArray in board.items():
                
        c = 0
        for chosenItem in columnArray:

            itemPosition = [(c*itemSize + innerSpacing*c + outerLeftMargin), (r*itemSize + innerSpacing*r + outerTopMargin)]
            itemSprite = Item(chosenItem, itemPosition, itemSize)

            itemGroup.add(itemSprite)
            c+=1

        r += 1

if len(board) > 0:
    testDict = True
    dictionaryLen = len(board)
else:
    testDict = False

if testDict == True:
    makeBoard(board)

else:
    for r in range(globs.ROW_COUNT):
        rowArray = []

        for c in range (globs.COLUMN_COUNT):
            itemCount = itemCount + 1

            chosenItem = itemTypes[random.randint(0, itemLen-1)]
            itemPosition = [(c*itemSize + innerSpacing*c + outerLeftMargin), (r*itemSize + innerSpacing*r + outerTopMargin)]
            
            rowArray.append(chosenItem)

            itemSprite = Item(chosenItem, itemPosition, itemSize)
            itemGroup.add(itemSprite)
            #maybe add it after calculations
        
        board[r] = rowArray

    #INCLUDE THIS in the function somehow


# Starting game
# board = create_board()
# draw_board(board)

itemCollect(board, itemTypes)

game_over = False
turn = 0

while not game_over:

    if down:
        h += 1
    
    def animateRemove(neededImages):
        print("helo")

    def animateMoveDown(neededImages):
        print("hiii")

    # event.button 1 -> left click
    # event.button 2 -> right click
    #event.button 3 -> middle click

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("hhh")
                if rectangle.collidepoint(event.pos):

                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y
                    print(offset_x)
                    print(offset_y)
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y   


    pygame.display.update()
    dt = clock.tick(FPS)
    itemGroup.draw(globs.SCREEN)

pygame.quit()
