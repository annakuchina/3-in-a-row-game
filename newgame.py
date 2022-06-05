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
import copy
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

#NEW
# board = {0: ['heal-potion', 'mushroom', 'tree', 'mushroom', 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'moon', 'mushroom'], 3: ['moon', 'snake', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'mushroom', 'tree']}


# board = {0: ['heal-potion', 'mushroom', 'tree', 'mushroom', 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'moon', 'mushroom'], 3: ['moon', 'snake', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'mushroom', 'tree']}



# 1 horizontal match
# board = {0: ["mushroom", 'mushroom', "mushroom", "snake", 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'moon', 'mushroom'], 3: ['moon', 'snake', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'mushroom', 'tree']}

# board = {0: ['heal-potion', 'mushroom', 'mushroom', 'mushroom', 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'snake', 'mushroom'], 3: ['moon', 'moon', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'tree', 'tree']}


#END SAMPLE BOARDS
#-----------------

# class Key(pygame.sprite.Sprite):
#     def __init__(self, xpos, ypos, id):
#         super(Key, self).__init__()
#         self.i

rectangle_draging = False
itemLen = len(itemTypes)
itemArray = []

# rectangle = pygame.rect.Rect(176, 134, 17, 17)

image = ""

allSprites = pygame.sprite.Group()
itemSize = [72, 72]
outlineSize = [72, 72]
innerSpacing = 10
outerTopMargin = 40
outerLeftMargin = 40
itemCount = 0

# spacingArray = [0, 0.2, 0.4, 0.6, 0.8, 1]


spacingArray = [0, 0.33333333, 0.66666666, 1]

# spacingArray = [1.33333, 1.33333, 1.66666, 1.66666]


pygame_icon = pygame.image.load(os.path.join("images", (str("mushroomScaled") + ".png"))).convert_alpha()
pygame.display.set_icon(pygame_icon)

itemDict = []

class Item(pygame.sprite.Sprite):
    def __init__(self):
        # super().__init__()
        pygame.sprite.Sprite.__init__(self)
        #Create all attributes


        # self.image = itemDict[chosenItem]
        # self.rect = self.image.get_rect()

        # self.rect.x = colNo*itemSize[0] + innerSpacing*colNo + outerLeftMargin  #put x coord here
        # self.rect.y = rowNo*itemSize[1] + innerSpacing*rowNo + outerTopMargin  #put y coord here

        # self.width = itemSize[0]
        # self.height = itemSize[1]
        # self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.image = image

        #CHANGE picture_path
        pass

        
        # BLUE_SPRITE = pygame.image.load(os.path.join("images", "blue.png")).convert_alpha()

    def setup(self):
        #  """ Load everything in and initialize attributes """

        self.mushroom = pygame.image.load(os.path.join("images", "mushroom.png")).convert_alpha()
        self.healPotion = pygame.image.load(os.path.join("images", "heal-potion.png")).convert_alpha()
        self.poisonPotion = pygame.image.load(os.path.join("images", "poison-potion.png")).convert_alpha()
        self.snake = pygame.image.load(os.path.join("images", "snake.png")).convert_alpha()
        self.moon = pygame.image.load(os.path.join("images", "moon.png")).convert_alpha()
        self.tree = pygame.image.load(os.path.join("images", "tree.png")).convert_alpha()

        self.orange = pygame.image.load(os.path.join("images", "orange.png")).convert_alpha()
        self.orangeSmaller = pygame.image.load(os.path.join("images", "orange-smaller.png")).convert_alpha()
        self.orangeSmall = pygame.image.load(os.path.join("images", "orange-small.png")).convert_alpha()

        self.blank = pygame.image.load(os.path.join("images", "BLANK.png")).convert_alpha()

        self.redOutline = pygame.image.load(os.path.join("images", "red-outline.png")).convert_alpha()
        self.whiteOutline = pygame.image.load(os.path.join("images", "white-outline.png")).convert_alpha()

        global itemDict
        itemDict ={"mushroom": self.mushroom,
        "heal-potion": self.healPotion,
        "poison-potion": self.poisonPotion,
        "snake": self.snake,
        "moon": self.moon,
        "tree": self.tree,

        "orange": self.orange,
        "orange-small": self.orangeSmall,
        "orange-smaller": self.orangeSmaller,

        "BLANK": self.blank,

        "red-outline": self.redOutline,
        "white-outline": self.whiteOutline
        }

    def drawItem(self, chosenItem, rowNo, colNo, itemSize):

        # if chosenItem == "BLANK":
        #     print("drawing blank")

        self.image = itemDict[chosenItem]
        self.rect = self.image.get_rect()

        self.rect.x = colNo*itemSize[0] + innerSpacing*colNo + outerLeftMargin  #put x coord here
        self.rect.y = rowNo*itemSize[1] + innerSpacing*rowNo + outerTopMargin  #put y coord here

        self.width = itemSize[0]
        self.height = itemSize[1]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        allSprites.add(self)
        # posX = colNo*itemSize[0] + innerSpacing*colNo + outerLeftMargin
        # posY = rowNo*itemSize[1] + innerSpacing*rowNo + outerTopMargin

        # itemPosition = [colNo*itemSize + innerSpacing*colNo + outerLeftMargin, ]
        # itemSprite = Item(chosenItem, itemPosition, itemSize)
        
    def drawItemDown(self, chosenItem, rowNo, colNo, itemSize, rowMultiplier):
        self.image = itemDict[chosenItem]
        self.rect = self.image.get_rect()

        self.rect.x = colNo*itemSize[0] + innerSpacing*colNo + outerLeftMargin
        self.rect.y = (rowNo+rowMultiplier)*itemSize[1] + innerSpacing*(rowNo+rowMultiplier) + outerTopMargin

        self.width = itemSize[0]
        self.height = itemSize[1]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # itemPosition = [posX, posY]
        
        #X, Y position

        #HERE
        allSprites.add(self)

# def wipeBoard():
#     itemSprite = Item()

# def positionGenerator()


scene = Item()
scene.setup()
pygame.time.delay(300)

def makeBoard(givenBoard):
    c = 0
    for c, colArray in givenBoard.items():
        r = 0
        for chosenItem in colArray:

            #Have to load in something for init

            scene = Item()

            scene.drawItem(chosenItem, r, c, itemSize)

            # itemGroup.add(itemSprite)
            
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

            # drawItem(chosenItem, r, c, itemSize)
            scene = Item()
            scene.drawItem(chosenItem, r, c, itemSize)

        
        board[c] = colArray


print(" ")
print(board)



# def drawItemDown(chosenItem, rowNo, colNo, itemSize, rowMultiplier):
    
#     posX = colNo*itemSize[0] + innerSpacing*colNo + outerLeftMargin
#     posY = (rowNo+rowMultiplier)*itemSize[1] + innerSpacing*(rowNo+rowMultiplier) + outerTopMargin

#     itemPosition = [posX, posY]
    
#     #X, Y position


#     #HERE
#     itemSprite = Item(chosenItem, itemPosition, itemSize)
#     allSprites.add(itemSprite)




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

    allSprites.draw(globs.SCREEN)

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
                        # drawItem(globs.deleteOrange[verticalRemoveCount//2], rowNo, key, itemSize)
                        scene = Item()
                        scene.drawItem(globs.deleteOrange[verticalRemoveCount//2], rowNo, key, itemSize)
        verticalRemoveCount += 1
        
    if removeHorizontal:
        for key in horizontalDict:
            for item in horizontalDict[key]:
                if isinstance(item, list):
                    for colNo in item:
                        # drawItem(globs.deleteOrange[horizontalRemoveCount//2], key, colNo, itemSize)
                        scene = Item()
                        scene.drawItem(globs.deleteOrange[horizontalRemoveCount//2], key, colNo, itemSize)
        horizontalRemoveCount += 1

    if shiftItemsDown:
        print(" ")
        print(shiftDownCount)
        print(board)
        #The unmoved board is getting made before the sprites are loaded in
        makeBoard(unmovedBoard)
        itemsModified = True

        for key in movedItemsBoard:
            unmovedRow = 0
            for item in unmovedBoard[key]:
                if item != "BLANK":
                    break

                unmovedRow += 1

            #COMMENTED OUT
            scene = Item()
            scene.drawItem("BLANK", 0, key, [itemSize[1], unmovedRow*itemSize[0] + (unmovedRow-1)*innerSpacing])
            

            for movedItem in movedItemsBoard[key]:
                selectedItem = board[key][movedItem]

                if movedItem == 0:
                    if "BLANK" not in board[key] and shiftDownCount==3:                
                        scene = Item()
                        scene.drawItem(selectedItem, movedItem, key, itemSize)
                    
                else:
                    scene = Item()
                    scene.drawItemDown(selectedItem, movedItem-1, key, itemSize, spacingArray[shiftDownCount//1])


        shiftDownCount += 1
    
    # redrawGameWindow == False

    pygame.display.update()


gameChanged = True
gameOver = False
turn = 0

shiftedDict = {}

removeHorizontal = False
removeVertical = False

itemDragging = False

selectedArray = []


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


    # if gameChanged == False:
    for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # print("hhh")

                    if removeVertical == False and removeHorizontal == False and shiftItemsDown == False:

                        itemSelected = True
                        mouse_x, mouse_y = event.pos

                        xLocation = mouse_x - outerLeftMargin

                        yLocation = mouse_y - outerTopMargin

                        # offset_x = mouse_x - outerTopMargin

                        # offset_y = rectangle.y - mouse_y



                        columnLocation = xLocation // (itemSize[0]+innerSpacing)
                        rowLocation = yLocation // (itemSize[1]+innerSpacing)

                        if columnLocation >= globs.COLUMN_COUNT or columnLocation < 0:
                            # print("jknd")
                            itemSelected = False
                        
                        if rowLocation >= globs.ROW_COUNT or rowLocation < 0:
                            # print("jknd")
                            itemSelected = False

                        # print("hi")
                        if itemSelected != False:
                            # print(selectedArray)
                            # print(len(selectedArray))

                            verticalDict = itemCollectVertical(board, itemTypes)
                            horizontalDict = itemCollectHorizontal(board, itemTypes)
                        
                            if len(selectedArray) == 0:
                                selectedArray.append([columnLocation, rowLocation])
                                scene = Item()
                                scene.drawItem("red-outline", rowLocation, columnLocation, itemSize)
                                pygame.display.update()
                            
                                # print("Drawn")

                                # print("column " + str(columnLocation))
                                # print("row " + str(rowLocation))
                                # print(" ")

                            elif len(selectedArray) == 1:
                                # There is 1 item currently selected
                                swappedBoard = copy.deepcopy(board)
                                
                                # The player selects the same position (row and column) twice
                                if selectedArray[0][0] == columnLocation and selectedArray[0][1] == rowLocation:
                                    scene = Item()
                                    scene.drawItem("white-outline", rowLocation, columnLocation, itemSize)
                                    # print("drawingWHTIE")
                                    selectedArray = []
                                    pygame.display.update()
                                
                                # elif selectedArray[0][0] == columnLocation

                                # Get range of possible locations

                                # print(selectedArray)
                                # print("akjhzdfj")
                                
                                # elif selectedArray[0][0] == columnLocation and selectedArray[0][0] - 1 == columnLocation:
                                #     print("ZDdjfs")
                                
                                

                                # NEED TO CHECK if the swapped icons would result in a match

                                # elif len(verticalDict) > 0 or len(horizontalDict) > 0:


                                #Two items are identical in a column (vertical)
                                elif selectedArray[0][0] == columnLocation and selectedArray[0][1] == rowLocation+1:
                                    swappedItems = True
                                    swappedBoard[columnLocation][rowLocation], swappedBoard[columnLocation][rowLocation+1] = swappedBoard[columnLocation][rowLocation+1], swappedBoard[columnLocation][rowLocation]

                                elif selectedArray[0][0] == columnLocation and selectedArray[0][1] == rowLocation-1:
                                    swappedItems = True
                                    swappedBoard[columnLocation][rowLocation], swappedBoard[columnLocation][rowLocation-1] = swappedBoard[columnLocation][rowLocation-1], swappedBoard[columnLocation][rowLocation]

                                #Two items are identical in a row (horizontal)
                                elif selectedArray[0][1] == rowLocation and selectedArray[0][0] == columnLocation+1:
                                    swappedItems = True
                                    swappedBoard[columnLocation][rowLocation], swappedBoard[columnLocation+1][rowLocation] = swappedBoard[columnLocation+1][rowLocation], swappedBoard[columnLocation][rowLocation]

                                elif selectedArray[0][1] == rowLocation and selectedArray[0][0] == columnLocation-1:
                                    swappedItems = True
                                    swappedBoard[columnLocation][rowLocation], swappedBoard[columnLocation-1][rowLocation] = swappedBoard[columnLocation-1][rowLocation], swappedBoard[columnLocation][rowLocation]

                                else:
                                    # print("WRONG")
                                    scene = Item()
                                    scene.drawItem("white-outline", selectedArray[0][1], selectedArray[0][0], itemSize)
                                    selectedArray = []
                                    selectedArray.append([columnLocation, rowLocation])

                                    scene = Item()
                                    scene.drawItem("red-outline", rowLocation, columnLocation, itemSize)
                                    pygame.display.update()

                                #If one of the 'swapped' conditions has been met

                                print(" ")
                                print(board)
                                print(swappedBoard)
                                if swappedBoard != board:
                                    verticalCollectedSwapped = itemCollectVertical(swappedBoard, itemTypes)
                                    horizontalCollectedSwapped = itemCollectHorizontal(swappedBoard, itemTypes)

                                    if len(verticalCollectedSwapped) > 0 or len(horizontalCollectedSwapped) > 0:
                                        # board = swappedBoard
                                        selectedArray = []
                                        gameChanged = True
                                        board = copy.deepcopy(swappedBoard)
                                        makeBoard(board)
                                        print("changed")
                                    

                                    # The items are not swapped
                                    else:
                                        scene = Item()
                                        scene.drawItem("white-outline", selectedArray[0][1], selectedArray[0][0], itemSize)
                                        selectedArray = []
                                    



                    # print(roundedNo)

                    # if xLocation > itemSize[0]:

                    #     print("out of bounds")

                    # print(xLocation)
                    # print(yLocation)


            # See if user has lifted the left mouse button
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    itemDragging = False

                    # See where the user drops the item
                    mouse_x, mouse_y = event.pos

                    newColumnLocation = (mouse_x-outerLeftMargin) // (itemSize[0]+innerSpacing)
                    newRowLocation = (mouse_y-outerTopMargin) // (itemSize[0]+innerSpacing)

                    
                    # See if its in the range of column and rows
                    


            # elif event.type == pygame.MOUSEMOTION:
            #     if itemDragging:
            #         mouse_x, mouse_y = event.pos

            #         columnLocation = (mouse_x-outerLeftMargin) // (itemSize[0]+innerSpacing)
            #         rowLocation = (mouse_y-outerTopMargin) // (itemSize[0]+innerSpacing)

            #         selectedItem Image***


                    # Find the item in the board dictionary
                    # Then move the item

                    # rectangle.x = mouse_x + offset_x
                    # rectangle.y = mouse_y + offset_y   


        # ONLY draw things in here
    redrawGameWindow()
        
        # if var1 == True:
        #     print(board)
        #     var1 = False
    

pygame.quit()