from operator import ne
from optparse import Values
import os, pygame, random, sys, math
from unicodedata import name
import numpy as np
from os import system
import time
import globs
from gameFunctions import itemCollectHorizontal, itemCollectVertical, shiftDown

# myFont = pygame.font.SysFont("monospace", 60)

clock = pygame.time.Clock()
FPS = 12
dt = clock.tick(FPS)

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


SQUARESIZE = 8
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
board = {0: ['purple', 'green', 'blue', 'yellow', 'purple', 'red', 'purple', 'green'], 1: ['yellow', 'blue', 'red', 'orange', 'blue', 'purple', 'green', 'green'], 2: ['yellow', 'purple', 'purple', 'purple', 'green', 'red', 'purple', 'green'], 3: ['red', 'blue', 'red', 'green', 'blue', 'blue', 'purple', 'blue'], 4: ['green', 'yellow', 'orange', 'orange', 'red', 'blue', 'green', 'yellow'], 5: ['green', 'blue', 'purple', 'green', 'green', 'green', 'blue', 'green'], 6: ['blue', 'blue', 'red', 'red', 'blue', 'blue', 'purple', 'green'], 7: ['purple', 'yellow', 'yellow', 'blue', 'red', 'yellow', 'yellow', 'blue']}

# 2 HORIZONTAL 4 in a row
# board = {0: ['purple', 'purple', 'green', 'yellow', 'green', 'purple', 'red', 'yellow'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'blue', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'orange', 'blue'], 3: ['green', 'red', 'purple', 'red', 'red', 'red', 'red', 'red'], 4: ['blue', 'blue', 'red', 'green', 'purple', 'blue', 'purple', 'orange'], 5: ['purple', 'green', 'green', 'yellow', 'blue', 'purple', 'green', 'green'], 6: ['yellow', 'green', 'green', 'green', 'green', 'purple', 'orange', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# board = {0: ['purple', 'purple', 'purple', 'yellow', 'green', 'purple', 'purple', 'purple'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'purple', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'purple', 'blue'], 3: ['green', 'red', 'purple', 'red', 'red', 'red', 'purple', 'red'], 4: ['blue', 'green', 'red', 'green', 'purple', 'blue', 'green', 'orange'], 5: ['green', 'green', 'green', 'blue', 'green', 'blue', 'purple', 'green'], 6: ['yellow', 'green', 'green', 'purple', 'green', 'purple', 'purple', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# board = {0: ['purple', 'purple', 'purple', 'yellow', 'green', 'purple', 'purple', 'purple'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'purple', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'purple', 'blue'], 3: ['green', 'red', 'purple', 'red', 'blue', 'red', 'purple', 'red'], 4: ['blue', 'green', 'red', 'green', 'purple', 'blue', 'green', 'orange'], 5: ['green', 'red', 'green', 'blue', 'green', 'blue', 'purple', 'green'], 6: ['yellow', 'green', 'green', 'purple', 'green', 'purple', 'blue', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# MULTIPLES
# board = {0: ['green', 'green', 'purple', 'green', 'yellow', 'yellow', 'purple', 'red'], 1: ['green', 'yellow', 'green', 'green', 'yellow', 'blue', 'blue', 'orange'], 2: ['green', 'red', 'yellow', 'purple', 'green', 'orange', 'yellow', 'blue'], 3: ['blue', 'blue', 'blue', 'purple', 'green', 'green', 'blue', 'green'], 4: ['purple', 'purple', 'red', 'yellow', 'yellow', 'green', 'green', 'blue'], 5: ['purple', 'blue', 'yellow', 'red', 'purple', 'blue', 'red', 'yellow'], 6: ['red', 'purple', 'yellow', 'blue', 'blue', 'green', 'yellow', 'purple'], 7: ['orange', 'red', 'yellow', 'green', 'blue', 'blue', 'yellow', 'red']}

#END SAMPLE BOARDS
#-----------------

# class Key(pygame.sprite.Sprite):
#     def __init__(self, xpos, ypos, id):
#         super(Key, self).__init__()
#         self.i

rectangle_draging = False
itemLen = len(itemTypes)
itemArray = []

rectangle = pygame.rect.Rect(176, 134, 17, 17)

image = ""

itemGroup = pygame.sprite.Group()
itemSize = 80
innerSpacing = 12
outerTopMargin = 40
outerLeftMargin = 40
itemCount = 0



class Item(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos, itemSize):
        super().__init__()


        completeImgPath = os.path.join("images", (str(picture_path) + ".png"))
        # add checking here later

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



def drawItem(chosenItem, rowNo, colNo, itemSize):
    itemPosition = [(colNo*itemSize + innerSpacing*colNo + outerLeftMargin), (rowNo*itemSize + innerSpacing*rowNo + outerTopMargin)]
    itemSprite = Item(chosenItem, itemPosition, itemSize)
    itemGroup.add(itemSprite)


def makeBoard(board):
    c = 0
    for c, colArray in board.items():
        r = 0
        for chosenItem in colArray:
            drawItem(chosenItem, r, c, itemSize)
            r+=1


if len(board) > 0:
    testDict = True
    dictionaryLen = len(board)
else:
    testDict = False

if testDict == True:
    makeBoard(board)

else:
    #Generate the board randomly
    for c in range(globs.COLUMN_COUNT):
        colArray = []

        for r in range(globs.ROW_COUNT):
            itemCount = itemCount + 1

            chosenItem = itemTypes[random.randint(0, globs.itemLen-1)]
            colArray.append(chosenItem)

            drawItem(chosenItem, r, c, itemSize)

        
        board[c] = colArray



# def replaceBlank:





horizontalRemoveCount = 0
verticalRemoveCount = 0


def redrawGameWindow():
    global firstGo
    global shiftedDict

    # global shiftedColCount
    # global shiftedCol

    global verticalRemoveCount
    global removeVertical

    global horizontalRemoveCount
    global removeHorizontal

    global board

    # globs.SCREEN.fill((255, 255, 255))
    #PUT BACKGROUND HERE LATER

    #THIS IS HOW THEY ARE DRAWN - the background images
    itemGroup.draw(globs.SCREEN)

    # IN the array, change the spaces to white
    #draw them again here

    if verticalRemoveCount + 1 >= 12:
        #3 sprites, display each for 3 frames = 9 total frames
        verticalRemoveCount = 0
        removeVertical = False

    if horizontalRemoveCount + 1 >= 12:
        horizontalRemoveCount = 0
        removeHorizontal = False

    if removeVertical:

        for key in verticalDict:
            for item in verticalDict[key]:
                if isinstance(item, list):
                    for rowNo in item:
                        drawItem(globs.deleteOrange[verticalRemoveCount//3], rowNo, key, itemSize)
        verticalRemoveCount += 1
        
    if removeHorizontal:
        for key in horizontalDict:
            for item in horizontalDict[key]:
                if isinstance(item, list):
                    for colNo in item:
                        drawItem(globs.deleteOrange[horizontalRemoveCount//3], key, colNo, itemSize)
        horizontalRemoveCount += 1


    if shiftItemsDown:
        print(shiftedDict)
        # DO the shifted down things
        pass

        # for key in board:
        #     if "BLANK" in board[key]:
        #         pass
        #         #PUT IT ALL HERE
        #         # newCol = shiftDown(key)


                


    pygame.display.update()



gameChanged = True
gameOver = False
turn = 0

shiftedDict = {}

removeHorizontal = False
removeVertical = False
shiftItemsDown = False

var1 = True

while not gameOver:
    clock.tick(FPS)
    
    # gameChanged = False

    # If the game is changed, check if there are vertical and horizontal matches, and then update them to disappear
    if gameChanged == True:
        verticalDict = itemCollectVertical(board, itemTypes)
        horizontalDict = itemCollectHorizontal(board, itemTypes)
        
        if len(verticalDict) > 0:
            removeVertical = True

            # print(board)
            for key in verticalDict:
                for item in verticalDict[key]:
                    if isinstance(item, list):
                        for rowNo in item:
                            board[key][rowNo] = "BLANK"

        else:
            removeVertical = False
            removeCount = 0
            verticalRemoveCount = 0
            

        if len(horizontalDict) > 0:
            removeHorizontal = True

            for key in horizontalDict:
                for item in horizontalDict[key]:
                    if isinstance(item, list):
                        for colNo in item:
                            board[colNo][key] = "BLANK"

        else:
            removeHorizontal = False
            removeCount = 0
            horizontalRemoveCount = 0

        gameChanged = False

    if var1:
        for key in board:
            if "BLANK" in board[key]:
                shiftItemsDown = True
                shiftedColCount, shiftedCol = shiftDown(board[key])

                shiftedDict[key] = [shiftedColCount, shiftedCol]

                # print("   ")
                # print(newCol)
                # print(changedColArray)

        var1 = False
            # PUT SOMETHING HERE


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


    # ONLY draw things in here
    redrawGameWindow()
    
    # if var1 == True:
    #     print(board)
    #     var1 = False
    

pygame.quit()
