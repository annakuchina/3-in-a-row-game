from operator import ne
from optparse import Values
import os, pygame, random, sys, math
from string import whitespace
from unicodedata import name
import numpy
from os import system
import time
# from connect_four_game.globs import COLUMN_COUNT
# from connect_four_game.globs import COLUMN_COUNT
import globs
from gameFunctions import itemCollectHorizontal, itemCollectVertical, shiftDown

# myFont = pygame.font.SysFont("monospace", 60)

clock = pygame.time.Clock()
FPS = 8
dt = clock.tick(FPS)

pygame.init()

globs.SCREEN.fill((255, 255, 255))
# globs.SCREEN.fill((0, 0, 0))

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
unmovedBoard = {}


left = 0
right = 0
up = 0
down = 0


shiftItemsDown = False

#-----------------
#SAMPLE BOARDS

# VERTICAL 3 in a row
# board = {0: ['purple', 'yellow', 'yellow', 'blue', 'orange', 'green', 'green', 'blue'], 1: ['purple', 'blue', 'yellow', 'blue', 'yellow', 'purple', 'orange', 'orange'], 2: ['yellow', 'orange', 'blue', 'green', 'orange', 'orange', 'red', 'green'], 3: ['blue', 'orange', 'green', 'blue', 'blue', 'green', 'green', 'yellow'], 4: ['blue', 'green', 'blue', 'orange', 'red', 'purple', 'purple', 'yellow'], 5: ['orange', 'yellow', 'orange', 'yellow', 'blue', 'yellow', 'orange', 'yellow'], 6: ['yellow', 'red', 'purple', 'purple', 'yellow', 'red', 'red', 'orange'], 7: ['yellow', 'red', 'blue', 'yellow', 'purple', 'blue', 'orange', 'blue']}
#Only 1
# board = {0: ['red', 'red', 'orange', 'green', 'yellow', 'purple', 'purple', 'blue'], 1: ['red', 'yellow', 'red', 'yellow', 'yellow', 'orange', 'green', 'blue'], 2: ['orange', 'red', 'red', 'yellow', 'green', 'orange', 'orange', 'red'], 3: ['red', 'red', 'orange', 'green', 'red', 'orange', 'red', 'yellow'], 4: ['yellow', 'yellow', 'blue', 'green', 'red', 'green', 'green', 'orange'], 5: ['orange', 'red', 'orange', 'yellow', 'orange', 'blue', 'orange', 'orange'], 6: ['blue', 'blue', 'orange', 'orange', 'blue', 'green', 'green', 'yellow'], 7: ['purple', 'yellow', 'yellow', 'orange', 'blue', 'red', 'yellow', 'green']}

# VERTICAL 4 in a row
# board = {0: ['blue', 'yellow', 'purple', 'purple', 'green', 'red', 'green', 'purple'], 1: ['blue', 'red', 'green', 'green', 'blue', 'orange', 'orange', 'orange'], 2: ['green', 'blue', 'red', 'orange', 'green', 'green', 'red', 'red'], 3: ['green', 'purple', 'purple', 'orange', 'red', 'blue', 'red', 'yellow'], 4: ['orange', 'purple', 'orange', 'blue', 'red', 'yellow', 'blue', 'blue'], 5: ['green', 'orange', 'purple', 'blue', 'red', 'blue', 'yellow', 'green'], 6: ['green', 'green', 'purple', 'orange', 'red', 'purple', 'yellow', 'orange'], 7: ['orange', 'green', 'red', 'blue', 'orange', 'yellow', 'blue', 'blue']}

# board = {0: ['red', 'blue', 'red', 'orange', 'orange', 'orange', 'green', 'green'], 1: ['red', 'blue', 'green', 'green', 'blue', 'green', 'orange', 'red'], 2: ['blue', 'green', 'blue', 'yellow', 'blue', 'orange', 'blue', 'orange'], 3: ['purple', 'purple', 'red', 'purple', 'yellow', 'orange', 'purple', 'yellow'], 4: ['green', 'green', 'blue', 'purple', 'green', 'blue', 'red', 'orange'], 5: ['blue', 'purple', 'green', 'yellow', 'yellow', 'orange', 'yellow', 'green'], 6: ['yellow', 'orange', 'blue', 'orange', 'green', 'purple', 'orange', 'green'], 7: ['purple', 'green', 'blue', 'yellow', 'purple', 'purple', 'red', 'blue']}


# HORIZONTAL 3 in a row
# board = {0: ['purple', 'green', 'blue', 'yellow', 'purple', 'red', 'purple', 'green'], 1: ['yellow', 'blue', 'red', 'orange', 'blue', 'purple', 'green', 'green'], 2: ['yellow', 'purple', 'purple', 'purple', 'green', 'red', 'purple', 'green'], 3: ['red', 'blue', 'red', 'green', 'blue', 'blue', 'purple', 'blue'], 4: ['green', 'yellow', 'orange', 'orange', 'red', 'blue', 'green', 'yellow'], 5: ['green', 'blue', 'purple', 'green', 'green', 'green', 'blue', 'green'], 6: ['blue', 'blue', 'red', 'red', 'blue', 'blue', 'purple', 'green'], 7: ['purple', 'yellow', 'yellow', 'blue', 'red', 'yellow', 'yellow', 'blue']}

# board = {0: ['purple', 'green', 'blue', 'yellow', 'purple', 'red', 'purple', 'green'], 1: ['yellow', 'blue', 'red', 'orange', 'blue', 'purple', 'green', 'green'], 2: ['yellow', 'purple', 'purple', 'purple', 'green', 'red', 'purple', 'green'], 3: ['red', 'blue', 'red', 'green', 'blue', 'blue', 'purple', 'blue'], 4: ['green', 'yellow', 'orange', 'orange', 'red', 'blue', 'green', 'yellow'], 5: ['green', 'blue', 'purple', 'green', 'green', 'green', 'blue', 'green'], 6: ['blue', 'blue', 'red', 'red', 'blue', 'blue', 'purple', 'green'], 7: ['purple', 'yellow', 'yellow', 'blue', 'red', 'yellow', 'yellow', 'blue']}


# 2 HORIZONTAL 4 in a row
# board = {0: ['purple', 'purple', 'green', 'yellow', 'green', 'purple', 'red', 'yellow'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'blue', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'orange', 'blue'], 3: ['green', 'red', 'purple', 'red', 'red', 'red', 'red', 'red'], 4: ['blue', 'blue', 'red', 'green', 'purple', 'blue', 'purple', 'orange'], 5: ['purple', 'green', 'green', 'yellow', 'blue', 'purple', 'green', 'green'], 6: ['yellow', 'green', 'green', 'green', 'green', 'purple', 'orange', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# board = {0: ['purple', 'purple', 'purple', 'yellow', 'green', 'purple', 'purple', 'purple'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'purple', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'purple', 'blue'], 3: ['green', 'red', 'purple', 'red', 'red', 'red', 'purple', 'red'], 4: ['blue', 'green', 'red', 'green', 'purple', 'blue', 'green', 'orange'], 5: ['green', 'green', 'green', 'blue', 'green', 'blue', 'purple', 'green'], 6: ['yellow', 'green', 'green', 'purple', 'green', 'purple', 'purple', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# board = {0: ['purple', 'purple', 'purple', 'yellow', 'green', 'purple', 'purple', 'purple'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'purple', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'purple', 'blue'], 3: ['green', 'red', 'purple', 'red', 'blue', 'red', 'purple', 'red'], 4: ['blue', 'green', 'red', 'green', 'purple', 'blue', 'green', 'orange'], 5: ['green', 'red', 'green', 'blue', 'green', 'blue', 'purple', 'green'], 6: ['yellow', 'green', 'green', 'purple', 'green', 'purple', 'blue', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# board = {0: ['purple', 'green', 'green', 'green', 'green', 'green', 'green', 'purple'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'purple', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'purple', 'blue'], 3: ['green', 'red', 'purple', 'red', 'blue', 'red', 'purple', 'red'], 4: ['blue', 'green', 'red', 'green', 'purple', 'blue', 'green', 'orange'], 5: ['green', 'red', 'green', 'blue', 'green', 'blue', 'purple', 'green'], 6: ['yellow', 'green', 'green', 'purple', 'green', 'purple', 'blue', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# board = {0: ['purple', 'green', 'green', 'green', 'green', 'green', 'green', 'purple'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'purple', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'green', 'blue'], 3: ['green', 'red', 'purple', 'red', 'blue', 'red', 'purple', 'red'], 4: ['blue', 'green', 'red', 'green', 'purple', 'blue', 'green', 'orange'], 5: ['green', 'red', 'green', 'blue', 'green', 'blue', 'purple', 'green'], 6: ['yellow', 'green', 'green', 'purple', 'green', 'purple', 'blue', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# board = {0: ['purple', 'green', 'green', 'green', 'purple', 'green', 'green', 'green'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'purple', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'green', 'blue'], 3: ['green', 'red', 'purple', 'red', 'blue', 'red', 'purple', 'red'], 4: ['blue', 'green', 'red', 'green', 'purple', 'blue', 'green', 'orange'], 5: ['green', 'red', 'green', 'blue', 'green', 'blue', 'purple', 'green'], 6: ['yellow', 'green', 'green', 'purple', 'green', 'purple', 'blue', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}



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
itemSize = [60, 60]
innerSpacing = 25
outerTopMargin = 40
outerLeftMargin = 70
itemCount = 0

# spacingArray = [0, 0.2, 0.4, 0.6, 0.8, 1]


spacingArray = [0, 0.33333333, 0.66666666, 1]

# spacingArray = [1.33333, 1.33333, 1.66666, 1.66666]


pygame_icon = pygame.image.load(os.path.join("images", (str("mushroomScaled") + ".png")))
pygame.display.set_icon(pygame_icon)


class Item(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos, itemSize):
        super().__init__()


        completeImgPath = os.path.join("images", (str(picture_path) + ".png"))
        # add checking here later
        # print(" ")
        # print(pos)

        self.image = pygame.image.load(completeImgPath)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]  #put x coord here
        self.rect.y = pos[1]  #put y coord here
        self.width = itemSize[0]
        self.height = itemSize[1]
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


# def drawCol(rowNo, colNo, itemSize):
#     itemPosition = [(colNo*itemSize + innerSpacing*colNo + outerLeftMargin), (rowNo*itemSize + innerSpacing*rowNo + outerTopMargin)]

#     itemSprite = Item("BLANK", rowNo, colNo, itemSize[0])




def drawItem(chosenItem, rowNo, colNo, itemSize):
    posX = colNo*itemSize[0] + innerSpacing*colNo + outerLeftMargin
    posY = rowNo*itemSize[1] + innerSpacing*rowNo + outerTopMargin

    # itemPosition = [colNo*itemSize + innerSpacing*colNo + outerLeftMargin, ]

    itemPosition = [posX, posY]
    itemSprite = Item(chosenItem, itemPosition, itemSize)
    itemGroup.add(itemSprite)


# def wipeBoard():
#     itemSprite = Item()

# def positionGenerator()


def makeBoard(givenBoard):
    c = 0
    for c, colArray in givenBoard.items():
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




def drawItemDown(chosenItem, rowNo, colNo, itemSize, rowMultiplier):
    
    posX = colNo*itemSize[0] + innerSpacing*colNo + outerLeftMargin
    posY = (rowNo+rowMultiplier)*itemSize[1] + innerSpacing*(rowNo+rowMultiplier) + outerTopMargin

    itemPosition = [posX, posY]
    
    #X, Y position

    itemSprite = Item(chosenItem, itemPosition, itemSize)
    itemGroup.add(itemSprite)




horizontalRemoveCount = 0
verticalRemoveCount = 0
shiftDownCount = 0

itemsModified = False



def redrawGameWindow():
    global firstGo
    global shiftedDict

    # global shiftedColCount
    # global shiftedCol

    global verticalRemoveCount
    global removeVertical

    global horizontalRemoveCount
    global removeHorizontal
    global itemsModified

    global shiftDownCount
    global shiftItemsDown
    global unmovedBoard
    global modifiedItems
    global movedItemsBoard

    global previousBoard

    global board

    itemGroup.draw(globs.SCREEN)

    if verticalRemoveCount + 1 >= 8:
        #4 sprites, display each for 2 frames = 8 total frames
        verticalRemoveCount = 0
        removeVertical = False

    if horizontalRemoveCount + 1 >= 8:
        horizontalRemoveCount = 0
        removeHorizontal = False

    if shiftDownCount + 1 >= 5:
        #Display 4 positions for 1 frames each = 4 frames
        shiftDownCount = 0
        shiftItemsDown = False
        # print("FALSE")
        # print(" ")

    if removeVertical:
        for key in verticalDict:
            for item in verticalDict[key]:
                if isinstance(item, list):
                    for rowNo in item:
                        drawItem(globs.deleteOrange[verticalRemoveCount//2], rowNo, key, itemSize)
        verticalRemoveCount += 1
        
    if removeHorizontal:
        for key in horizontalDict:
            for item in horizontalDict[key]:
                if isinstance(item, list):
                    for colNo in item:
                        drawItem(globs.deleteOrange[horizontalRemoveCount//2], key, colNo, itemSize)
        horizontalRemoveCount += 1

    if shiftItemsDown:
        makeBoard(unmovedBoard)
        itemsModified = True

        for key in movedItemsBoard:
            unmovedRow = 0
            for item in unmovedBoard[key]:
                if item != "BLANK":
                    break

                unmovedRow += 1

            drawItem("BLANK", 0, key, [itemSize[1], unmovedRow*itemSize[0] + (unmovedRow-1)*innerSpacing])
            
            for movedItem in movedItemsBoard[key]:
                selectedItem = board[key][movedItem]

                if movedItem == 0:
                    if "BLANK" not in board[key] and shiftDownCount==3:                
                        drawItem(selectedItem, movedItem, key, itemSize)
                    
                else:
                    drawItemDown(selectedItem, movedItem-1, key, itemSize, spacingArray[shiftDownCount//1])


        shiftDownCount += 1
    
    # redrawGameWindow == False


    pygame.display.update()



gameChanged = True
gameOver = False
turn = 0

shiftedDict = {}

removeHorizontal = False
removeVertical = False


shiftedBoard = {}
droppedItemsDict = {}

var1 = True


while not gameOver:   
    clock.tick(FPS)

    # If the game is changed, check if there are vertical and horizontal matches, and then update them to disappear
    if gameChanged == True and shiftItemsDown == False:
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


    if removeVertical == False and removeHorizontal == False and shiftItemsDown == False:
        blankCount = 0

        unmovedBoard = {}
        movedItemsBoard = {}

        if var1 == True:
            for key in board:
                if "BLANK" in board[key]:
                    shiftItemsDown = True
                    blankCount += 1
                    modifiedItems, unchangedCol, shiftedCol = shiftDown(board[key])
                    movedItemsBoard[key] = modifiedItems
                    board[key] = shiftedCol
                    unmovedBoard[key] = unchangedCol

        if blankCount == 0:
            shiftItemsDown = False


    if itemsModified == True and shiftItemsDown == False:
        gameChanged = True
        itemsModified = False



    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("hhh")
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
