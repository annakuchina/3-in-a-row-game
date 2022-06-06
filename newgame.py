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

screenDimensions = [925, 840] 


#-----------------
#SAMPLE BOARDS

#no matches
# board = {0: ['mushroom', 'moon', 'tree', 'snake', 'tree', 'poison-potion', 'poison-potion', 'heal-potion'], 1: ['mushroom', 'poison-potion', 'tree', 'poison-potion', 'heal-potion', 'mushroom', 'tree', 'mushroom'], 2: ['moon', 'moon', 'mushroom', 'heal-potion', 'tree', 'snake', 'moon', 'heal-potion'], 3: ['tree', 'tree', 'snake', 'poison-potion', 'poison-potion', 'mushroom', 'moon', 'heal-potion'], 4: ['tree', 'poison-potion', 'moon', 'snake', 'tree', 'tree', 'mushroom', 'moon'], 5: ['snake', 'moon', 'mushroom', 'poison-potion', 'snake', 'heal-potion', 'mushroom', 'poison-potion'], 6: ['mushroom', 'mushroom', 'snake', 'poison-potion', 'mushroom', 'snake', 'tree', 'poison-potion'], 7: ['heal-potion', 'tree', 'poison-potion', 'mushroom', 'tree', 'heal-potion', 'tree', 'moon']}

#NEW
# board = {0: ['heal-potion', 'mushroom', 'tree', 'mushroom', 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'moon', 'mushroom'], 3: ['moon', 'snake', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'mushroom', 'tree']}


# board = {0: ['heal-potion', 'mushroom', 'tree', 'mushroom', 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'moon', 'mushroom'], 3: ['moon', 'snake', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'mushroom', 'tree']}



# 1 horizontal match
# board = {0: ["mushroom", 'mushroom', "mushroom", "snake", 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'moon', 'mushroom'], 3: ['moon', 'snake', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'mushroom', 'tree']}

# board = {0: ['heal-potion', 'mushroom', 'mushroom', 'mushroom', 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'snake', 'mushroom'], 3: ['moon', 'moon', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'tree', 'tree']}


#END SAMPLE BOARDS
#-----------------

uiColor = (209, 209, 255)
uiColor = (6, 136, 87)
uiColor = (0, 0, 0)
uiColor = (16, 18, 28)
uiColor = (201, 234, 208)
uiColor = (255, 226, 209)

uiColor = (247, 199, 173)
uiColor = (247, 187, 150)

# uiColor = (245, 200, 171)

# darkerGreen = (150, 204, 161)

# darkerGreen = (148, 211, 160)

# darkerGreen = (252, 153, 95)

whiteColor = (255, 255, 255)

darkerGreen = (6, 136, 87)
# darkerGreen = (103, 175, 234)
darkerGreen = (249, 155, 52)
darkerGreen = (247, 146, 51)

darkerGreen = (249, 155, 52)
# darkerGreen = (239, 125, 71)

darkerOrange = (255, 155, 68)

darkerGreen = (255, 174, 99)

# uiColor = (187, 232, 196)

accentColor = (255, 255, 255)

# lighterBgColor = (255, 243, 237)
# lighterBgColor = (252, 126, 0)

rectangle_draging = False
itemLen = len(itemTypes)
itemArray = []


image = ""

allSprites = pygame.sprite.Group()
itemSize = [72, 72]
outlineSize = [72, 72]
innerSpacing = 9
outerTopMargin = 155
outerLeftMargin = 75
itemCount = 0

spacingArray = [0, 0.33333333, 0.66666666, 1]

pygame_icon = pygame.image.load(os.path.join("images", (str("mushroomScaled") + ".png"))).convert_alpha()
pygame.display.set_icon(pygame_icon)

itemDict = []



class Item(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def setup(self):
        #  Load everything in and initialize attributes
        print("Loading in")
        self.mushroom = pygame.image.load(os.path.join("images", "mushroom.png")).convert()
        self.healPotion = pygame.image.load(os.path.join("images", "heal-potion.png")).convert()
        self.poisonPotion = pygame.image.load(os.path.join("images", "poison-potion.png")).convert()
        self.snake = pygame.image.load(os.path.join("images", "snake.png")).convert()
        self.moon = pygame.image.load(os.path.join("images", "moon.png")).convert()
        self.tree = pygame.image.load(os.path.join("images", "tree.png")).convert()

        self.orange = pygame.image.load(os.path.join("images", "orange.png")).convert()
        self.orangeSmaller = pygame.image.load(os.path.join("images", "orange-smaller.png")).convert()
        self.orangeSmall = pygame.image.load(os.path.join("images", "orange-small.png")).convert()

        self.blank = pygame.image.load(os.path.join("images", "BLANK.png")).convert()

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

    def drawItem(self, chosenItem, rowNo, colNo, itemSize, rowMultiplier):
        self.image = itemDict[chosenItem]
        self.rect = self.image.get_rect()

        self.rect.x = colNo*itemSize[0] + innerSpacing*colNo + outerLeftMargin  #put x coord here
        self.rect.y = (rowNo+rowMultiplier)*itemSize[1] + innerSpacing*(rowNo+rowMultiplier) + outerTopMargin  #put y coord here

        self.width = itemSize[0]
        self.height = itemSize[1]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        allSprites.add(self)

    def drawSidebarItems(self, item, count):
            print(item)
            print(itemTypes)
            self.image = itemDict[item]
            self.rect = self.image.get_rect()

            self.rect.x = globs.COLUMN_COUNT*itemSize[0] + innerSpacing*globs.COLUMN_COUNT + outerLeftMargin + 30

            #Space it equal distances from the top
            self.rect.y = count*70 + 2*itemSize[1] + outerTopMargin
            # self.rect.y = i*50 + 2*itemSize[1] + innerSpacing*2 + outerTopMargin

            self.width = 40
            self.height = 40

            self.image = pygame.transform.scale(self.image, (self.width, self.height))

            allSprites.add(self)

    # def drawSidebarLines(self):
        

# class UI(pygame.sprite.Sprite):

# Set up the game
scene = Item()
scene.setup()
pygame.time.delay(1000)



def drawSidebar():

    sidebarLeftSpacing = 30
    sideBarWidth = 90

    # rect_object = pygame.Rect(globs.COLUMN_COUNT * itemSize[0] + outerLeftMargin + 200, 0, 500, 1000)
    # pygame.draw.rect(globs.SCREEN, uiColor, rect_object)
    
    # print(screenDimensions[1])
    

    #Draw the orange background
    rect_object = pygame.Rect(0, 0, screenDimensions[0], screenDimensions[1])
    pygame.draw.rect(globs.SCREEN, uiColor, rect_object)


    # topBarBg = pygame.Rect(outerLeftMargin, 35, screenDimensions[0]-(2*outerLeftMargin), 90)

    topBarBg = pygame.Rect(outerLeftMargin, 35, globs.COLUMN_COUNT*itemSize[1]+(globs.COLUMN_COUNT-1)*innerSpacing + sidebarLeftSpacing + sideBarWidth, 90)
    pygame.draw.rect(globs.SCREEN, whiteColor, topBarBg)
    #Draw the top bar
    
    # topBar = pygame.Rect(outerLeftMargin, 30, screenDimensions[0]-(2*outerLeftMargin), 90)
    topBar = pygame.Rect(outerLeftMargin+5, 40, screenDimensions[0]-(2*outerLeftMargin)-10, 80)
    pygame.draw.rect(globs.SCREEN, darkerOrange, topBar)


    # rect_object = pygame.Rect(globs.COLUMN_COUNT * itemSize[0] + outerLeftMargin + 200, outerTopMargin + 2*(itemSize[1] + outerTopMargin), 500, 100)
    # pygame.draw.rect(globs.SCREEN, accentColor, rect_object)

    #Draw the right side bar


    sideBarBg = pygame.Rect(outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing)+ sidebarLeftSpacing, outerTopMargin, sideBarWidth+10, (itemSize[1])*globs.COLUMN_COUNT + innerSpacing*(globs.COLUMN_COUNT-1))
    pygame.draw.rect(globs.SCREEN, whiteColor, sideBarBg)


    sideBar = pygame.Rect(outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing)+sidebarLeftSpacing+5, outerTopMargin+5, sideBarWidth, (itemSize[1])*globs.COLUMN_COUNT + innerSpacing*(globs.COLUMN_COUNT-1)-10)
    # sideBar = pygame.Rect(outerLeftMargin, 30, screenDimensions[0]-(2*outerLeftMargin), 80)
    pygame.draw.rect(globs.SCREEN, darkerGreen, sideBar)

    i = 0
    for item in itemTypes:
        scene = Item()
        scene.drawSidebarItems(item, i)

        i+=1

drawSidebar()




def makeBoard(givenBoard):
    c = 0
    for c, colArray in givenBoard.items():
        r = 0
        for chosenItem in colArray:

            scene = Item()
            scene.drawItem(chosenItem, r, c, itemSize, 0)
            
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

            scene = Item()
            scene.drawItem(chosenItem, r, c, itemSize, 0)

        
        board[c] = colArray


horizontalRemoveCount = 0
verticalRemoveCount = 0
shiftDownCount = 0

itemsModified = False


# print(board)


def redrawGameWindow():
    global firstGo
    global shiftedDict

    global verticalRemoveCount
    global removeVertical

    global horizontalRemoveCount
    global removeHorizontal
    global itemsModified

    global shiftDownCount
    global shiftItemsDown

    global unmovedBoard
    global movedItemsBoard

    global previousBoard

    global board

    allSprites.draw(globs.SCREEN)

    if verticalRemoveCount + 1 >= 9:
        #4 sprites, display each for 2 frames = 8 total frames
        verticalRemoveCount = 0
        removeVertical = False

    if horizontalRemoveCount + 1 >= 9:
        horizontalRemoveCount = 0
        removeHorizontal = False

    if shiftDownCount + 1 >= 5:
        #Display 4 positions for 1 frames each = 4 total frames
        shiftDownCount = 0
        shiftItemsDown = False

    if removeVertical:
        for key in verticalDict:
            for item in verticalDict[key]:
                if isinstance(item, list):
                    for rowNo in item:
                        scene = Item()
                        scene.drawItem(globs.deleteOrange[verticalRemoveCount//2], rowNo, key, itemSize, 0)
        verticalRemoveCount += 1
        
    if removeHorizontal:
        for key in horizontalDict:
            for item in horizontalDict[key]:
                if isinstance(item, list):
                    for colNo in item:
                        scene = Item()
                        scene.drawItem(globs.deleteOrange[horizontalRemoveCount//2], key, colNo, itemSize, 0)
        horizontalRemoveCount += 1

    if shiftItemsDown:
        # Old sprites are being emptied, the unmoved board is created
        allSprites.empty()
        makeBoard(unmovedBoard)
        itemsModified = True

        for key in movedItemsBoard:
            unmovedRow = 0
            for item in unmovedBoard[key]:
                if item != "BLANK":
                    break

                unmovedRow += 1

            scene = Item()


            #Draw the background in

            #Key is column
            scene.drawItem("BLANK", 0, key, [itemSize[1], unmovedRow*itemSize[0] + (unmovedRow-1)*innerSpacing], 0)

            # rect_object = pygame.Rect(key*itemSize[0]+innerSpacing*(key)+outerLeftMargin, outerTopMargin, itemSize[1], unmovedRow*itemSize[0] + (unmovedRow-1)*innerSpacing)
            # allSprites.add(rect_object)
            # Needs to be added into queue but not added yet

            # pygame.draw.rect(globs.SCREEN, uiColor, rect_object)


            for movedItem in movedItemsBoard[key]:
                selectedItem = board[key][movedItem]

                if movedItem == 0:
                    if "BLANK" not in board[key] and shiftDownCount==3:                
                        scene = Item()
                        scene.drawItem(selectedItem, movedItem, key, itemSize, 0)
                    
                else:
                    scene = Item()
                    scene.drawItem(selectedItem, movedItem-1, key, itemSize, spacingArray[shiftDownCount//1])

        shiftDownCount += 1
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


while not gameOver:   
    clock.tick(FPS)

    # If the game is changed, check if there are vertical and horizontal matches, and then update them to disappear
    if gameChanged == True and shiftItemsDown == False:
        verticalDict = itemCollectVertical(board, itemTypes)
        horizontalDict = itemCollectHorizontal(board, itemTypes)
        
        if len(verticalDict) > 0:
            removeVertical = True

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

                    if removeVertical == False and removeHorizontal == False and shiftItemsDown == False:

                        itemSelected = True
                        mouse_x, mouse_y = event.pos

                        xLocation = mouse_x - outerLeftMargin
                        yLocation = mouse_y - outerTopMargin

                        columnLocation = xLocation // (itemSize[0]+innerSpacing)
                        rowLocation = yLocation // (itemSize[1]+innerSpacing)

                        if columnLocation >= globs.COLUMN_COUNT or columnLocation < 0:
                            itemSelected = False
                        
                        if rowLocation >= globs.ROW_COUNT or rowLocation < 0:
                            itemSelected = False

                        if itemSelected != False:
                            verticalDict = itemCollectVertical(board, itemTypes)
                            horizontalDict = itemCollectHorizontal(board, itemTypes)
                        
                            if len(selectedArray) == 0:
                                selectedArray.append([columnLocation, rowLocation])
                                scene = Item()
                                scene.drawItem("red-outline", rowLocation, columnLocation, itemSize, 0)
                                pygame.display.update()

                            elif len(selectedArray) == 1:
                                # There is 1 item currently selected
                                swappedItems = False
                                swappedBoard = copy.deepcopy(board)
                                
                                # The player selects the same position (row and column) twice
                                if selectedArray[0][0] == columnLocation and selectedArray[0][1] == rowLocation:
                                    scene = Item()
                                    scene.drawItem("white-outline", rowLocation, columnLocation, itemSize, 0)
                                    selectedArray = []
                                    pygame.display.update()

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
                                    scene = Item()
                                    scene.drawItem("white-outline", selectedArray[0][1], selectedArray[0][0], itemSize, 0)
                                    selectedArray = []
                                    selectedArray.append([columnLocation, rowLocation])

                                    scene = Item()
                                    scene.drawItem("red-outline", rowLocation, columnLocation, itemSize, 0)
                                    pygame.display.update()

                                # If one of the 'swapped' conditions has been met
                                if swappedItems == True:
                                    verticalCollectedSwapped = itemCollectVertical(swappedBoard, itemTypes)
                                    horizontalCollectedSwapped = itemCollectHorizontal(swappedBoard, itemTypes)

                                    if len(verticalCollectedSwapped) > 0 or len(horizontalCollectedSwapped) > 0:
                                        selectedArray = []
                                        gameChanged = True
                                        board = copy.deepcopy(swappedBoard)
                                        makeBoard(board)
                                        print("changed")
                                    
                                    elif swappedBoard[selectedArray[0][0]][selectedArray[0][1]] == board[selectedArray[0][0]][selectedArray[0][1]]:
                                        print("SAME THING")
                                        scene.drawItem("white-outline", selectedArray[0][1], selectedArray[0][0], itemSize, 0)
                                        selectedArray = []

                                    # The items are not swapped
                                    else:
                                        scene = Item()
                                        scene.drawItem("white-outline", selectedArray[0][1], selectedArray[0][0], itemSize, 0)
                                        selectedArray = []

            # See if user has lifted the left mouse button
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    itemDragging = False

                    # See where the user drops the item
                    mouse_x, mouse_y = event.pos

                    # See if it's in the range of column and rows
                    newColumnLocation = (mouse_x-outerLeftMargin) // (itemSize[0]+innerSpacing)
                    newRowLocation = (mouse_y-outerTopMargin) // (itemSize[0]+innerSpacing)

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

    # Drawing the game
    redrawGameWindow()

pygame.quit()