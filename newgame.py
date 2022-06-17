import os, pygame, random, sys, math
from re import T

import globs
import copy
from gameFunctions import itemCollectHorizontal, itemCollectVertical, shiftDown

clock = pygame.time.Clock()
FPS = 8

pygame.init()
pygame_icon = pygame.image.load(os.path.join("images", (str("mushroomScaled") + ".png"))).convert_alpha()
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('Woodland')

pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN])

globs.SCREEN.fill((255, 255, 255))
mainFont = pygame.font.Font(os.path.join("fonts","prstartk.ttf"), 16)
headingFont = pygame.font.Font(os.path.join("fonts","prstartk.ttf"), 35)
biggerHeadingFont = pygame.font.Font(os.path.join("fonts","prstartk.ttf"), 41)

fontS2 = 30
fontS3 = 50
fontS1 = 16
gameRunning = True


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
playerStatsModified = False
screenDimensions = [925, 840] 

whiteColor = (255, 255, 255)
blackColor = (0, 0, 0)
backgroundPeachColor = (247, 187, 150)
darkerOrangeColor = (255, 155, 68)
lighterOrangeColor = (255, 174, 99)
backgroundLighterOrangeColor = (252, 196, 136)


# mushroomSimpleColor = (232, 50, 49)
mushroomSimpleColor = (241, 60, 62)

# treeSimpleColor = (246, 82, 48)
treeSimpleColor = (246, 107, 47)

# healPotionSimpleColor = (202, 18, 81)
# snakeSimpleColor = (88, 102, 229)
# moonSimpleColor = (175, 72, 238)
# poisonPotionSimpleColor = (15, 130, 85)


rectangle_draging = False
itemLen = len(itemTypes)
image = ""
allSprites = pygame.sprite.Group()
itemSize = [72, 72]
outlineSize = [72, 72]
innerSpacing = 8
outerTopMargin = 155
outerLeftMargin = 50
itemCount = 0

spacingArray = [0, 0.33333333, 0.66666666, 1]

sidebarLeftSpacing = 30
sideBarWidth = 155

itemsDrawn = False
fullPlayerStatsList = []


#-----------------
#SAMPLE BOARDS


board = {0: ['mushroom', 'poisonPotion', 'moon', 'mushroom', 'poisonPotion', 'mushroom', 'snake', 'tree'], 1: ['tree', 'healPotion', 'moon', 'healPotion', 'mushroom', 'mushroom', 'tree', 'healPotion'], 2: ['healPotion', 'healPotion', 'snake', 'moon', 'poisonPotion', 'mushroom', 'poisonPotion', 'healPotion'], 3: ['healPotion', 'tree', 'tree', 'snake', 'mushroom', 'mushroom', 'healPotion', 'mushroom'], 4: ['tree', 'mushroom', 'mushroom', 'poisonPotion', 'snake', 'mushroom', 'poisonPotion', 'mushroom'], 5: ['mushroom', 'poisonPotion', 'mushroom', 'healPotion', 'tree', 'healPotion', 'tree', 'mushroom'], 6: ['moon', 'mushroom', 'mushroom', 'snake', 'moon', 'healPotion', 'tree', 'mushroom'], 7: ['tree', 'healPotion', 'tree', 'snake', 'moon', 'snake', 'healPotion', 'tree']}

# board = {0: ['mushroom', 'tree', 'tree', 'snake', 'tree', 'poisonPotion', 'poisonPotion', 'healPotion'], 1: ['mushroom', 'tree', 'mushroom', 'poisonPotion', 'healPotion', 'mushroom', 'tree', 'mushroom'], 2: ['moon', 'moon', 'tree', 'healPotion', 'tree', 'snake', 'moon', 'healPotion'], 3: ['tree', 'mushroom', 'snake', 'poisonPotion', 'poisonPotion', 'mushroom', 'moon', 'healPotion'], 4: ['tree', 'poisonPotion', 'moon', 'snake', 'tree', 'tree', 'mushroom', 'moon'], 5: ['snake', 'moon', 'mushroom', 'poisonPotion', 'snake', 'healPotion', 'mushroom', 'poisonPotion'], 6: ['mushroom', 'mushroom', 'snake', 'poisonPotion', 'mushroom', 'snake', 'tree', 'poisonPotion'], 7: ['healPotion', 'tree', 'poisonPotion', 'mushroom', 'tree', 'healPotion', 'tree', 'moon']}
# board = {0: ['mushroom', 'tree', 'tree', 'tree', 'tree', 'tree', 'tree', 'tree'], 1: ['mushroom', 'tree', 'mushroom', 'poisonPotion', 'healPotion', 'mushroom', 'tree', 'mushroom'], 2: ['moon', 'moon', 'tree', 'healPotion', 'tree', 'tree', 'tree', 'healPotion'], 3: ['tree', 'mushroom', 'snake', 'poisonPotion', 'poisonPotion', 'mushroom', 'moon', 'healPotion'], 4: ['tree', 'poisonPotion', 'moon', 'snake', 'tree', 'tree', 'mushroom', 'moon'], 5: ['snake', 'moon', 'mushroom', 'poisonPotion', 'snake', 'healPotion', 'mushroom', 'poisonPotion'], 6: ['mushroom', 'mushroom', 'snake', 'poisonPotion', 'mushroom', 'snake', 'tree', 'poisonPotion'], 7: ['healPotion', 'tree', 'poisonPotion', 'mushroom', 'tree', 'healPotion', 'tree', 'moon']}

# board = {0: ['snake', 'snake', 'snake', 'poisonPotion', 'poisonPotion', 'snake', 'mushroom', 'mushroom'], 1: ['mushroom', 'mushroom', 'moon', 'moon', 'poisonPotion', 'snake', 'tree', 'mushroom'], 2: ['tree', 'snake', 'snake', 'mushroom', 'poisonPotion', 'moon', 'poisonPotion', 'tree'], 3: ['tree', 'snake', 'moon', 'snake', 'moon', 'mushroom', 'poisonPotion', 'snake'], 4: ['tree', 'poisonPotion', 'snake', 'healPotion', 'snake', 'moon', 'mushroom', 'moon'], 5: ['snake', 'healPotion', 'poisonPotion', 'snake', 'tree', 'tree', 'poisonPotion', 'mushroom'], 6: ['mushroom', 'mushroom', 'healPotion', 'mushroom', 'poisonPotion', 'mushroom', 'tree', 'poisonPotion'], 7: ['healPotion', 'healPotion', 'mushroom', 'mushroom', 'snake', 'moon', 'tree', 'moon']}

# board = {0: ['snake', 'snake', 'tree', 'mushroom', 'mushroom', 'moon', 'mushroom', 'snake'], 1: ['snake', 'poisonPotion', 'healPotion', 'moon', 'healPotion', 'mushroom', 'poisonPotion', 'poisonPotion'], 2: ['healPotion', 'snake', 'mushroom', 'moon', 'tree', 'healPotion', 'healPotion', 'poisonPotion'], 3: ['mushroom', 'tree', 'tree', 'poisonPotion', 'mushroom', 'moon', 'snake', 'healPotion'], 4: ['moon', 'healPotion', 'moon', 'moon', 'moon', 'poisonPotion', 'mushroom', 'healPotion'], 5: ['poisonPotion', 'snake', 'poisonPotion', 'snake', 'poisonPotion', 'healPotion', 'snake', 'poisonPotion'], 6: ['healPotion', 'poisonPotion', 'moon', 'healPotion', 'moon', 'tree', 'moon', 'moon'], 7: ['snake', 'mushroom', 'snake', 'poisonPotion', 'snake', 'snake', 'poisonPotion', 'moon']}

#no matches
# board = {0: ['mushroom', 'moon', 'tree', 'snake', 'tree', 'poison-potion', 'poison-potion', 'heal-potion'], 1: ['mushroom', 'poison-potion', 'tree', 'poison-potion', 'heal-potion', 'mushroom', 'tree', 'mushroom'], 2: ['moon', 'moon', 'mushroom', 'heal-potion', 'tree', 'snake', 'moon', 'heal-potion'], 3: ['tree', 'tree', 'snake', 'poison-potion', 'poison-potion', 'mushroom', 'moon', 'heal-potion'], 4: ['tree', 'poison-potion', 'moon', 'snake', 'tree', 'tree', 'mushroom', 'moon'], 5: ['snake', 'moon', 'mushroom', 'poison-potion', 'snake', 'heal-potion', 'mushroom', 'poison-potion'], 6: ['mushroom', 'mushroom', 'snake', 'poison-potion', 'mushroom', 'snake', 'tree', 'poison-potion'], 7: ['heal-potion', 'tree', 'poison-potion', 'mushroom', 'tree', 'heal-potion', 'tree', 'moon']}
# board = {0: ['tree', 'moon', 'tree', 'snake', 'tree', 'poison-potion', 'poison-potion', 'heal-potion'], 1: ['tree', 'poison-potion', 'tree', 'poison-potion', 'heal-potion', 'mushroom', 'tree', 'mushroom'], 2: ['moon', 'tree', 'mushroom', 'tree', 'tree', 'snake', 'moon', 'heal-potion'], 3: ['tree', 'tree', 'snake', 'poison-potion', 'poison-potion', 'mushroom', 'moon', 'heal-potion'], 4: ['tree', 'poison-potion', 'moon', 'snake', 'tree', 'tree', 'mushroom', 'moon'], 5: ['snake', 'moon', 'mushroom', 'poison-potion', 'snake', 'heal-potion', 'mushroom', 'poison-potion'], 6: ['mushroom', 'mushroom', 'snake', 'poison-potion', 'mushroom', 'snake', 'tree', 'poison-potion'], 7: ['heal-potion', 'tree', 'poison-potion', 'mushroom', 'tree', 'heal-potion', 'tree', 'moon']}

#NEW
# board = {0: ['heal-potion', 'mushroom', 'tree', 'mushroom', 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'moon', 'mushroom'], 3: ['moon', 'snake', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'mushroom', 'tree']}
# board = {0: ['heal-potion', 'mushroom', 'tree', 'mushroom', 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'moon', 'mushroom'], 3: ['moon', 'snake', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'mushroom', 'tree']}
# 1 horizontal match
# board = {0: ["mushroom", 'mushroom', "mushroom", "snake", 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'moon', 'mushroom'], 3: ['moon', 'snake', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'mushroom', 'tree']}
# board = {0: ['heal-potion', 'mushroom', 'mushroom', 'mushroom', 'tree', 'tree', 'mushroom', 'moon'], 1: ['moon', 'tree', 'snake', 'moon', 'tree', 'heal-potion', 'snake', 'heal-potion'], 2: ['mushroom', 'mushroom', 'heal-potion', 'moon', 'snake', 'moon', 'snake', 'mushroom'], 3: ['moon', 'moon', 'moon', 'heal-potion', 'poison-potion', 'snake', 'snake', 'poison-potion'], 4: ['heal-potion', 'mushroom', 'snake', 'mushroom', 'tree', 'moon', 'mushroom', 'snake'], 5: ['tree', 'snake', 'heal-potion', 'tree', 'snake', 'moon', 'snake', 'heal-potion'], 6: ['moon', 'heal-potion', 'moon', 'moon', 'snake', 'mushroom', 'snake', 'mushroom'], 7: ['snake', 'poison-potion', 'snake', 'poison-potion', 'poison-potion', 'tree', 'tree', 'tree']}
#END SAMPLE BOARDS
#-----------------





class Item(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
    def setup(self):
        #  Load everything in and initialize attributes
        self.mushroomTransparent = pygame.image.load(os.path.join("images", "mushroomTransparent.png")).convert_alpha()
        self.treeTransparent = pygame.image.load(os.path.join("images", "treeTransparent.png")).convert_alpha()

        self.pauseButton = pygame.image.load(os.path.join("images", "pauseButton.png")).convert_alpha()

        self.mushroom = pygame.image.load(os.path.join("images", "mushroom.png")).convert()
        self.healPotion = pygame.image.load(os.path.join("images", "healPotion.png")).convert()
        self.poisonPotion = pygame.image.load(os.path.join("images", "poisonPotion.png")).convert()
        self.snake = pygame.image.load(os.path.join("images", "snake.png")).convert()
        self.moon = pygame.image.load(os.path.join("images", "moon.png")).convert()
        self.tree = pygame.image.load(os.path.join("images", "tree.png")).convert()
        
        self.heart = pygame.image.load(os.path.join("images", "heart.png")).convert_alpha()
        self.heartHalf = pygame.image.load(os.path.join("images", "heartHalf.png")).convert_alpha()
        self.energy = pygame.image.load(os.path.join("images", "energy.png")).convert_alpha()
        self.energyHalf = pygame.image.load(os.path.join("images", "energyHalf.png")).convert_alpha()

        self.mushroomSimple = pygame.image.load(os.path.join("images", "mushroomSimple.png")).convert_alpha()
        self.healPotionSimple = pygame.image.load(os.path.join("images", "healPotionSimple.png")).convert_alpha()
        self.poisonPotionSimple = pygame.image.load(os.path.join("images", "poisonPotionSimple.png")).convert_alpha()
        self.snakeSimple = pygame.image.load(os.path.join("images", "snakeSimple.png")).convert_alpha()
        self.moonSimple = pygame.image.load(os.path.join("images", "moonSimple.png")).convert_alpha()
        self.treeSimple = pygame.image.load(os.path.join("images", "treeSimple.png")).convert_alpha()

        self.selectedOutline = pygame.image.load(os.path.join("images", "selectedOutline.png")).convert_alpha()
        self.deselectedOutline = pygame.image.load(os.path.join("images", "deselectedOutline.png")).convert_alpha()

        self.collectionBorder = pygame.image.load(os.path.join("images", "collectionBorder.png")).convert_alpha()
        self.collectionBorderRed = pygame.image.load(os.path.join("images", "collectionBorderRed.png")).convert_alpha()
        self.collectionBorderOrange = pygame.image.load(os.path.join("images", "collectionBorderOrange.png")).convert_alpha()

        self.blank = pygame.image.load(os.path.join("images", "BLANK.png")).convert()
        self.blankDynamic = pygame.image.load(os.path.join("images", "BLANKDynamic.png")).convert_alpha()
        self.blankSidebar = pygame.image.load(os.path.join("images", "BLANKSidebar.png")).convert()
        
        global itemDict
        global mushroomSimpleColor, treeSimpleColor

        itemDict ={
        "mushroomTransparent": self.mushroomTransparent,
        "treeTransparent": self.treeTransparent,

        "pauseButton": self.pauseButton,
        
        "mushroom": self.mushroom,
        "healPotion": self.healPotion,
        "poisonPotion": self.poisonPotion,
        "snake": self.snake,
        "moon": self.moon,
        "tree": self.tree,

        "heart": self.heart,
        "heartHalf": self.heartHalf,
        "energy": self.energy,
        "energyHalf": self.energyHalf,
        
        "mushroomSimple": self.mushroomSimple,
        "healPotionSimple": self.healPotionSimple,
        "poisonPotionSimple": self.poisonPotionSimple,
        "snakeSimple": self.snakeSimple,
        "moonSimple": self.moonSimple,
        "treeSimple": self.treeSimple,

        "selectedOutline": self.selectedOutline,
        "deselectedOutline": self.deselectedOutline,

        "collectionBorder": self.collectionBorder,
        "collectionBorderRed": self.collectionBorderRed,
        "collectionBorderOrange": self.collectionBorderOrange,
        
        "BLANK": self.blank,
        "BLANKDynamic": self.blankDynamic,
        "blankSidebar": self.blankSidebar
        }
        global playerStats
        playerStats = {
            # 0 index: order in which the item is in display, 1: the previous count of items, 2: the current count of items
            "heart": [0, 3, 3],
            "energy": [1, 3, 3]
        }
        global itemCountDict
        # 0 index: order in which the item is display, 1: the previous count of items, 2: the current count of items, 3: the required tally of items, 4: the colour corresponding to the item
        itemCountDict = {
        "mushroomSimple": [0, 0, 0, 4, mushroomSimpleColor],
        "treeSimple": [1, 0, 0, 6, treeSimpleColor],
        "healPotionSimple": [2, 0, 0, 9, (202, 18, 81)],
        "snakeSimple": [3, 0, 0, 7, (88, 102, 229)],
        "moonSimple": [4, 0, 0, 8, (175, 72, 238)],
        "poisonPotionSimple": [5, 0, 0, 8, (15, 130, 85)]
        }

        
        
    def drawItem(self, item, xLocation, yLocation, width, height):
        self.image = itemDict[item]
        self.rect = self.image.get_rect()
        self.rect.x = xLocation
        self.rect.y = yLocation
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        allSprites.add(self)
       
# Set up the game
scene = Item()
scene.setup()


def drawGridItem(chosenItem, rowNo, colNo, givenItemSize, rowMultiplier):
    xLocation = colNo*givenItemSize[0] + innerSpacing*colNo + outerLeftMargin
    yLocation = (rowNo+rowMultiplier)*givenItemSize[1] + innerSpacing*(rowNo+rowMultiplier) + outerTopMargin
    width = givenItemSize[0]
    height = givenItemSize[1]
    scene = Item()
    scene.drawItem(chosenItem, xLocation, yLocation, width, height)


def makeBoard(givenBoard):
    print("Making a board")
    c = 0
    for c, colArray in givenBoard.items():
        r = 0
        for chosenItem in colArray:
            drawGridItem(chosenItem, r, c, itemSize, 0)
            
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
            drawGridItem(chosenItem, r, c, itemSize, 0)
        
        board[c] = colArray

print(board)


def drawItemCount(item):
    global itemsDrawn
    # print(itemCountDict)
    # print("FDJDJ")
    itemCountMessage = str(itemCountDict[item][1]) + "/" + str(itemCountDict[item][3])
    xTextLocation = outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + 67
    yTextLocation = itemCountDict[item][0]*55 + 2.5*itemSize[1] + outerTopMargin - fontS1 + 25
    
    textColor = ""

    #Add a different color if it is full
    if itemCountDict[item][2] == itemCountDict[item][3]:
        textColor = itemCountDict[item][4]

    if itemCountDict[item][0] > 1:
        yTextLocation += 55
    
    if itemCountDict[item][0] > 2:
        yTextLocation += 35
        if textColor == "":
            textColor = blackColor
    else:
        if textColor == "":
            textColor = whiteColor

    


    #If icons have already been drawn, cover over them with the background color to clear them
    if itemsDrawn == True:
        text_surface = mainFont.render(itemCountMessage, False, lighterOrangeColor)
        globs.SCREEN.blit(text_surface, (xTextLocation, yTextLocation))
        itemCountMessage = str(itemCountDict[item][2]) + "/" + str(itemCountDict[item][3])
        
    text_surface = mainFont.render(itemCountMessage, False, textColor)
    globs.SCREEN.blit(text_surface, (xTextLocation, yTextLocation))
    itemsDrawn = True

def calculatePlayerStats(item, itemNumber):
    global fullPlayerStatsList
    # Take the number that needs to be added/subtracted, and to it
    
    #Prev count
    # if itemCountDict[item][1] == itemCountDict[item][3]:
    # See if there is 4/4 etc and then make the energy and stuff go up
    # User reached the required amount of items
    if itemCountDict[item][2] + itemNumber >= itemCountDict[item][3]:
        itemCountDict[item][1] = itemCountDict[item][2]
        itemCountDict[item][2] = itemCountDict[item][3]
        # print(item)
        fullPlayerStatsList.append(item)
        #The icons are drawn in here
        drawItemCount(item)
    
     # User has not reached the required amount of items yet
    elif itemCountDict[item][2] != itemCountDict[item][3]:
        itemCountDict[item][1] = itemCountDict[item][2]
        itemCountDict[item][2] += itemNumber
        drawItemCount(item)
    
    if itemCountDict[item][2] == 0:
        gameOver = True
        print("game over")
        # showGameOverScreen(gameOver)
        
        #Do things depending on if its a good or bad item
    # drawItemCount(item)
        

def drawSidebarIcons():
    # Drawing all the simpler, smaller icons in the sidebar
    width = 30
    height = 30
    for item in itemCountDict:
        count = itemCountDict[item][0]
        xLocation = outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + 23
        yLocation = count*55 + 2.5*itemSize[1] + outerTopMargin
        scene = Item()

        if count > 1:
            yLocation += 55

        if count > 2:
            yLocation += 35

        #Friendlies

        if count == 0:
            drawText("+", 60, darkerOrangeColor, xLocation + 22, yLocation - 50)
            drawText("+", 40, whiteColor, xLocation + 32, yLocation - 41)
        
        #Enemies
        elif count == 3:
            drawText("x", 56, darkerOrangeColor, xLocation + 22 + 3 + 4, yLocation - 49 - 3)
            drawText("x", 40, blackColor, xLocation + 32 + 4, yLocation - 41 - 3 + 1)

        scene.drawItem(item, xLocation, yLocation, width, height)

        drawItemCount(item)

    allSprites.draw(globs.SCREEN)


# def drawCollection


def clearPlayerStats(item):
    scene = Item()
    xLocation = outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + 20 + sidebarLeftSpacing
    yLocation = 2*itemSize[0]/3 + outerTopMargin + playerStats[item][0]*40
    width = 3*30 + 2*10
    height = 30
    item = "BLANK"
    scene.drawItem(item, xLocation, yLocation, width, height)

#DRAW the energy and heart icons


def drawPlayerStats(item, itemNumber):
    #EDIT this to cover only the needed ones (at the very end)
    playerStats[item][1] = playerStats[item][2]
    playerStats[item][2] += itemNumber
    selectedItem = item

    # There are less items there than there were previously
    if playerStats[item][2] < playerStats[item][1]:
        clearPlayerStats(item)
        print("clear")

    i = 0
    width = 30
    height = 30
    while i < playerStats[item][2]:
        scene = Item()
        xLocation = outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + 20 + sidebarLeftSpacing + math.floor(i)*40
        yLocation = 2*itemSize[0]/3 + outerTopMargin + playerStats[item][0]*40
        if i + 0.5 == playerStats[item][2]:
            selectedItem = selectedItem + "Half"
        elif i + 0.25 == playerStats[item][2] and playerStats[item][1] % 1 == 0.5:
            selectedItem = selectedItem + "Half"
        
        scene.drawItem(selectedItem, xLocation, yLocation, width, height)
        i += 1

    allSprites.draw(globs.SCREEN)


def fillCollection(item):

    # scene.drawItem("collectionBorder", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + 30, 2*55 + 2.5*itemSize[1] + outerTopMargin - 5, 40, 40)
    # scene.drawItem("collectionBorder", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + (sideBarWidth - 40) - 30, 2*55 + 2.5*itemSize[1] + outerTopMargin - 5, 40, 40)
    scene = Item()

    if item == "mushroomSimple":
        fillUpNumber = 10
        currentFillStatus = 0

        print("mushroom")
        mushroomCollectionBg = pygame.Rect(outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + 25 + 6, (45 - fillUpNumber - currentFillStatus) + (2*55 + 2.5*itemSize[1] + outerTopMargin - 7), 45 -12, fillUpNumber)
        pygame.draw.rect(globs.SCREEN, mushroomSimpleColor, mushroomCollectionBg)

        scene.drawItem("collectionBorderRed", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing +25, 2*55 + 2.5*itemSize[1] + outerTopMargin - 7, 45, 45)
    

    elif item == "treeSimple":
        fillUpNumber = 10
        currentFillStatus = 0

        print("tree")

        treeCollectionBg = pygame.Rect(outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + (sideBarWidth - 45) - 25 + 6, (45 - fillUpNumber - currentFillStatus) +  (2*55 + 2.5*itemSize[1] + outerTopMargin - 7), 45 - 12, 10)
        pygame.draw.rect(globs.SCREEN, treeSimpleColor, treeCollectionBg)

        scene.drawItem("collectionBorderOrange", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + (sideBarWidth - 45) - 25, 2*55 + 2.5*itemSize[1] + outerTopMargin - 7, 45, 45)



def drawSidebar():
    #Draw the orange background
    rect_object = pygame.Rect(0, 0, screenDimensions[0], screenDimensions[1])
    pygame.draw.rect(globs.SCREEN, backgroundPeachColor, rect_object)

    #Draw the top bar
    topBarBg = pygame.Rect(outerLeftMargin, 35, globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth, 90)
    pygame.draw.rect(globs.SCREEN, whiteColor, topBarBg)
    topBar = pygame.Rect(outerLeftMargin+5, 40, globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth - 10, 80)
    pygame.draw.rect(globs.SCREEN, darkerOrangeColor, topBar)

    #Draw the right side bar
    sideBarBg = pygame.Rect(outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing)+ sidebarLeftSpacing, outerTopMargin, sideBarWidth, (itemSize[1])*globs.COLUMN_COUNT + innerSpacing*(globs.COLUMN_COUNT-1))
    pygame.draw.rect(globs.SCREEN, whiteColor, sideBarBg)
    sideBar = pygame.Rect(outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing)+sidebarLeftSpacing+5, outerTopMargin+5, sideBarWidth-10, (itemSize[1])*globs.COLUMN_COUNT + innerSpacing*(globs.COLUMN_COUNT-1)-10)
    pygame.draw.rect(globs.SCREEN, lighterOrangeColor, sideBar)

    textMessage = "Woodland"
    drawCenterText(textMessage, 50, pinkColor, screenDimensions[0]/2 + 4 + 5, outerTopMargin/2 + 6)
    # drawCenterText(textMessage, 50, redColor, screenDimensions[0]/2+3, outerTopMargin/2 + 5)
    drawCenterText(textMessage, 50, whiteColor, screenDimensions[0]/2 + 5, outerTopMargin/2 + 6)

    scene = Item()

    levelNumber = 1
    drawText("L" + str(levelNumber), 40, whiteColor, outerLeftMargin+50, 62)
    # drawText(str(levelNumber), 50, whiteColor, outerLeftMargin+50, 60)
    
    scene.drawItem("pauseButton", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth/3 + 5, 58, 50, 50)

    # xLocation = outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + 20 + sidebarLeftSpacing
    # yLocation = 2*itemSize[0]/3 + outerTopMargin + playerStats[item][0]*40
    # width = 3*30 + 2*10
    # height = 30
    # color = whiteColor

    # statBg = pygame.Rect(outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + 10 + sidebarLeftSpacing, 2*itemSize[0]/3 + outerTopMargin - 10, 3*30 + 2*10 + 20, 90)
    # pygame.draw.rect(globs.SCREEN, darkerOrangeColor, statBg)



    # scene.drawItem(item, xLocation, yLocation, width, height)
    
    # scene = Item()
    # scene.drawItem("collectionBorder", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + 30, 2*55 + 2.5*itemSize[1] + outerTopMargin - 5, 40, 40)

    fillCollection("mushroomSimple")
    # scene.drawItem("collectionBorder", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + 30, outerTopMargin + (globs.COLUMN_COUNT-1)*(itemSize[1]+innerSpacing) - 20, 40, 40)

    # scene = Item()
    # scene.drawItem("collectionBorder", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + (sideBarWidth - 40) - 30, 2*55 + 2.5*itemSize[1] + outerTopMargin - 5, 40, 40)

    fillCollection("treeSimple")
    # scene.drawItem("collectionBorder", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + (sideBarWidth - 40) - 30, outerTopMargin + (globs.COLUMN_COUNT-1)*(itemSize[1]+innerSpacing) - 20, 40, 40)


    # scene = Item()
    # scene.drawItem("playButton", globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth, 53, 65, 65)

    # pygame.draw.polygon(surface=globs.SCREEN, color=(255,0,0), points=[(50,100), (100,50), (150,100)])
    # text_surface = biggerHeadingFont.render(textMessage, False, whiteColor)
    # globs.SCREEN.blit(text_surface, (xTextLocation, yTextLocation + 20))





displayedArray = []


horizontalRemoveCount = 0
verticalRemoveCount = 0
shiftDownCount = 0
itemsModified = False

addItemBorder = False
removeItemBorder = False

modifyEnergy = 0
modifyHearts = 0


boardChanged = False
boardChanged = False

previousShiftDownCount = -1

previousRemoveVerticalCount = -1
previousRemoveHorizontalCount = -1

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
    global horizontalDict, verticalDict
    global previousBoard
    global board
    global addItemBorder, removeItemBorder
    global selectedArray, displayedArray
    global modifyEnergy
    global boardChanged, boardChanged
    global startLevel
    global fullPlayerStatsList
    global modifyHearts

    global previousShiftDownCount, previousRemoveVerticalCount, previousRemoveHorizontalCount

    if verticalRemoveCount + 1 >= 5:
        #3 sprites, display each for 4 frames = 8 total frames
        verticalRemoveCount = 0
        removeVertical = False

    if horizontalRemoveCount + 1 >= 5:
        horizontalRemoveCount = 0
        removeHorizontal = False

    if shiftDownCount + 1 >= 5:
        #Display 2 positions for 2 frames each = 4 total frames
        shiftDownCount = 0
        shiftItemsDown = False
        # previousShiftDownCount = 0

    if removeVertical:
        if previousRemoveVerticalCount != verticalRemoveCount//2:
            for key in verticalDict:
                for item in verticalDict[key]:
                    if isinstance(item, list):
                        # print(item)
                        for rowNo in item:
                            drawGridItem(globs.deleteAnimation[verticalRemoveCount//2], rowNo, key, itemSize, 0)
                            boardChanged = True

        previousRemoveVerticalCount = verticalRemoveCount
        verticalRemoveCount += 1

        # itemBoardChanged = True
        
    if removeHorizontal:
        if previousRemoveHorizontalCount != horizontalRemoveCount//2:
            for key in horizontalDict:
                for item in horizontalDict[key]:
                    if isinstance(item, list):
                        for colNo in item:
                            drawGridItem(globs.deleteAnimation[horizontalRemoveCount//2], key, colNo, itemSize, 0)
                            boardChanged = True


        previousRemoveHorizontalCount = horizontalRemoveCount
        horizontalRemoveCount += 1

    if shiftItemsDown:
        # Old sprites are being emptied, the shifted down board is created
        allSprites.empty()
        boardChanged = True

        for key in movedItemsBoard:
            unmovedRow = 0
            for item in unmovedBoard[key]:
                if item != "BLANK":
                    break
                unmovedRow += 1
            #Draw the background in
            #The unmoved grid is being drawn, after which the blank spaces in between are drawn, and then the items are drawn

            
            drawGridItem("BLANK", 0, key, [itemSize[1], unmovedRow*itemSize[0] + (unmovedRow-1)*innerSpacing], 0)
            for movedItem in movedItemsBoard[key]:
                selectedItem = board[key][movedItem]
                if movedItem == 0:
                    if "BLANK" not in board[key] and shiftDownCount==3: 
                        drawGridItem(selectedItem, movedItem, key, itemSize, 0)
                        itemsModified = True
                        #Switching the item above for the one below
                    
                else:
                        drawGridItem(selectedItem, movedItem-1, key, itemSize, spacingArray[shiftDownCount//1])
                        itemsModified = True

        shiftDownCount += 1


    if removeItemBorder:
        drawGridItem("deselectedOutline", displayedArray[0][1], displayedArray[0][0], itemSize, 0)
        
        displayedArray = []
        removeItemBorder = False
        # print("CHANGED startlevel")
        
        boardChanged = True


    if addItemBorder:
        drawGridItem("selectedOutline", selectedArray[0][1], selectedArray[0][0], itemSize, 0)
        startLevel = False

        addItemBorder = False
        displayedArray = selectedArray

        selectedArray = []

        boardChanged = True

    if modifyEnergy != 0:
        drawPlayerStats("energy", modifyEnergy)
        modifyEnergy = 0

        boardChanged = True

    # if len(fullPlayerStatsList) > 0 and shiftItemsDown == False and removeHorizontal == False and removeVertical == False:
    if len(fullPlayerStatsList) > 0 and gameChanged == True:
        # if 
        # print(" ")
        #Get this to run after the items fall
        
        for item in fullPlayerStatsList:
            # print(fullPlayerSta tsList)

            # Friendly items
            if item == "mushroomSimple":
                fillCollection(item)
                modifyEnergy = 1
                modifyHearts = 1

            elif item == "treeSimple":
                fillCollection(item)
                modifyEnergy = 1
                modifyHearts = 0.5
                # if 3 - playerStats["energy"][2] == 0:
                #     pass
                    #ADD the counting up in here
                

            elif item == "healPotionSimple":

                modifyEnergy = 3
                modifyHearts = 3

                # if playerStats["energy"][2] < 3:
                #     drawPlayerStats("energy", 3 - playerStats["energy"][2])

                # if playerStats["heart"][2] < 3:
                #     drawPlayerStats("heart", 3 - playerStats["heart"][2])

            # Enemy items
            elif item == "snakeSimple":
                # pass
                modifyEnergy = -1

            elif item == "moonSimple":
                # pass
                modifyHearts = -0.5

            elif item == "poisonPotionSimple":
                # pass
                modifyEnergy = -0.5
                modifyHearts = -1


            if modifyEnergy > 0:
                if modifyEnergy + playerStats["energy"][2] >= 3:
                    drawPlayerStats("energy", 3 - playerStats["energy"][2])

                else:
                    drawPlayerStats("energy", modifyEnergy)

            elif modifyEnergy < 0:
                # modifyEnergy takes away more energy than is available (player loses)
                if -modifyEnergy >= playerStats["energy"][2]:
                    print("YOU LOST")
                    sys.exit()
                else:
                    drawPlayerStats("energy", modifyEnergy)


            if modifyHearts > 0:
                if modifyHearts + playerStats["heart"][2] > 3:
                    drawPlayerStats("heart", 3 - playerStats["heart"][2])
                else:
                    drawPlayerStats("heart", modifyHearts)

            elif modifyHearts < 0:
                # modifyHearts takes away more hearts than are available (player loses)
                if -modifyHearts >= playerStats["heart"][2]:
                    print("YOU LOST")
                    sys.exit()
                else:
                    drawPlayerStats("heart", modifyHearts)


            modifyEnergy = 0
            modifyHearts = 0

            itemCountDict[item][1] = itemCountDict[item][2]
            itemCountDict[item][2] = 0
            drawItemCount(item)

        fullPlayerStatsList = []
            #LEN and a true variable

        boardChanged = True
        

    if boardChanged:
        allSprites.draw(globs.SCREEN)
        pygame.display.update()
        boardChanged = False


gameChanged = False
gameOver = False
turn = 0
shiftedDict = {}
removeHorizontal = False
removeVertical = False
itemDragging = False
selectedArray = []
shiftedBoard = {}
droppedItemsDict = {}

# def showGameOverScreen(gameOver):
#     while gameOver:
#         clock.tick(FPS)
#         # scene = Item()
#         # scene.setup()
#         rect_object = pygame.Rect(0, 0, screenDimensions[0], screenDimensions[1])
#         pygame.draw.rect(globs.SCREEN, whiteColor, rect_object)
#         # allSprites.draw(globs.SCREEN)
#         pygame.display.update()
#         # redrawGameWindow()
#     # self.screen.blit()

gameOver = False
# mainMenuRunning = True
# gameRunning = False
# # showGameOverScreen(gameOver)
# menuCreated = False
# def createMenu():
#     global menuCreated
#     menuCreated = True
#     rect_object = pygame.Rect(0, 0, screenDimensions[0], screenDimensions[1])
#     pygame.draw.rect(globs.SCREEN, whiteColor, rect_object)

last_pos = (0, 0)
# Play Screen
def play(): 
    global gameChanged, shiftItemsDown, board, itemsModified, selectedArray, removeCount, verticalRemoveCount, horizontalRemoveCount, removeVertical, removeHorizontal
    global horizontalDict, verticalDict, movedItemsBoard, unmovedBoard, last_pos
    allSprites.empty()
    makeBoard(board)
    drawSidebar()
    drawPlayerStats("heart", 0)
    drawPlayerStats("energy", 0)
    drawSidebarIcons()
    
        # for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             sys.exit()
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             if event.button == 1:
        #                 pass
                        
redColor = (226, 39, 38)
# redColor = (239, 50, 50)
greenColor = (4, 73, 52)
pinkColor = (216, 30, 92)
lighterPinkColor = (242, 50, 111)
brighterOrangeColor = (255, 151, 48)
orangeRedColor = (245, 75, 42)
orangeRedColor = (244, 121, 44)
babyBlueColor = (79, 109, 225)
darkBlueColor = (52, 67, 177)
purpleColor = (195, 105, 223)
purpleColor = (189, 99, 217)
brighterPurpleColor = (201, 86, 239)

def drawCenterText(displayText, textSize, textColor, xBackgroundWidth, yLocation):
    font = pygame.font.Font(os.path.join("fonts","prstartk.ttf"), textSize)
    textSurface = font.render(displayText, False, textColor)
    textRect = textSurface.get_rect(center = (xBackgroundWidth, yLocation))
    globs.SCREEN.blit(textSurface, textRect)

def drawText(displayText, textSize, textColor, xLocation, yLocation):
    font = pygame.font.Font(os.path.join("fonts","prstartk.ttf"), textSize)
    textSurface = font.render(displayText, False, textColor)
    globs.SCREEN.blit(textSurface, (xLocation, yLocation))

def button(textContent, xLocation, yLocation, width, height, backgroundColor, textColor, textSize):
    pygame.draw.rect(globs.SCREEN, backgroundColor, (xLocation, yLocation, width, height))
    drawCenterText(textContent, textSize, textColor, width//2 + xLocation, height//2 + yLocation)
    
def quitGame():
    pygame.quit()
    quit()

def pauseMenu():
    global last_pos
    allSprites.empty()
    globs.SCREEN.fill(backgroundPeachColor)
    screenTitle = "Pause"
    drawCenterText(screenTitle, 80, whiteColor, screenDimensions[0]//2, 2.7*screenDimensions[1]/10)
    button("Resume", (screenDimensions[0]- 400)//2, 3.5*screenDimensions[1]/10, 400, 90, whiteColor, lighterPinkColor, 30)
    button("Help", (screenDimensions[0]- 375)//2, 5*screenDimensions[1]/10, 375, 90, whiteColor, brighterOrangeColor, 30)
    button("Quit", (screenDimensions[0]- 330)//2, 6.6*screenDimensions[1]/10, 330, 90, whiteColor, brighterPurpleColor, 30)

    # allSprites.draw(globs.Screen)
    # print("FDSKJJK")
    # pygame.display.update()

def helpMenu():
    global last_pos
    allSprites.empty()
    #Thinner green border
    globs.SCREEN.fill(lighterOrangeColor)


def mainMenu():
    global last_pos
    allSprites.empty()
    rectObject = pygame.Rect(0, 0, screenDimensions[0], screenDimensions[1])
    pygame.draw.rect(globs.SCREEN, darkerOrangeColor, rectObject)
    rectObject = pygame.Rect(40, 40, screenDimensions[0]-80, screenDimensions[1]-80)
    pygame.draw.rect(globs.SCREEN, whiteColor, rectObject)
    gameTitle = "Woodland"
    drawCenterText(gameTitle, 80, redColor, screenDimensions[0]//2, 3.5*screenDimensions[1]/10)
    scene = Item()
    scene.drawItem("mushroomTransparent", 2*screenDimensions[0]/10, 1.4*screenDimensions[1]/10, 150, 150)
    scene = Item()
    scene.drawItem("treeTransparent", 7*screenDimensions[0]/10, 3.9*screenDimensions[1]/10, 150, 150)
    button("Start", (screenDimensions[0]- 250)//2, 4.5*screenDimensions[1]/10, 250, 70, lighterPinkColor, whiteColor, 25)
    button("Help", (screenDimensions[0]- 225)//2, 5.7*screenDimensions[1]/10, 225, 70, darkerOrangeColor, whiteColor, 25)
    button("Quit", (screenDimensions[0]- 200)//2, 7*screenDimensions[1]/10, 200, 70, purpleColor, whiteColor, 25)

    allSprites.draw(globs.SCREEN)


gameRunning = False
gameRunning = True

mainMenuRunning = True
pauseMenuRunning = False
helpMenuRunning = False

playScreenRunning = False

initiateScreen = True
startLevel = True

while gameRunning:

    mouse_pos = pygame.mouse.get_pos()
    if (mouse_pos != last_pos):
        mouse_x, mouse_y = mouse_pos
        last_pos = mouse_pos

    if playScreenRunning:

        # print("playscreenrun")

        if initiateScreen:
            print("initiating")
            play()
            # pygame.display.update()
            # print(allSprites)
            # allSprites.draw(globs.SCREEN)
            initiateScreen = False
            pygame.display.update()
            gameChanged = True


        mouse_pos = pygame.mouse.get_pos()
        if (mouse_pos != last_pos):
            mouse_x, mouse_y = mouse_pos
            last_pos = mouse_pos


        # If the game is changed, check if there are vertical and horizontal matches, and then update them to disappear
        if gameChanged == True and shiftItemsDown == False:
            verticalDict = itemCollectVertical(board, itemTypes)
            horizontalDict = itemCollectHorizontal(board, itemTypes)
 
            if len(verticalDict) > 0:
                removeVertical = True
                for key in verticalDict:
                    for item in verticalDict[key]:
                        if isinstance(item, list):
                            # Check that it's not 3 blank's in a row
                                matchItem = board[key][item[0]]
                                matchLength = len(item)
                                if startLevel == False:
                                    if matchItem != "BLANK":
                                        calculatePlayerStats(matchItem + "Simple", matchLength)
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
                                matchItem = board[item[0]][key]
                                matchLength = len(item)
                                if startLevel == False:
                                    if matchItem != "BLANK":
                                        calculatePlayerStats(matchItem + "Simple", matchLength)
                                for colNo in item:
                                    board[colNo][key] = "BLANK"
            else:
                removeHorizontal = False
                removeCount = 0
                horizontalRemoveCount = 0

            gameChanged = False

            # redrawGameWindow()
            # pygame.display.update()

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

        redrawGameWindow()

    elif mainMenuRunning:
        if initiateScreen:
            mainMenu()
            pygame.display.update()
            initiateScreen = False

    elif pauseMenuRunning:
        if initiateScreen:
            print("HIHJFD")
            pauseMenu()
            pygame.display.update()
            initiateScreen = False

    elif helpMenuRunning:
        if initiateScreen:
            helpMenu()
            pygame.display.update()
            initiateScreen = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if mainMenuRunning:
                    #Resume
                    # print("clicked on main menu")
                    if (screenDimensions[0]- 250)//2 + 250 > mouse_x > (screenDimensions[0]- 250)//2 and 4.5*screenDimensions[1]/10 + 70 > mouse_y > 4.5*screenDimensions[1]/10:
                        mainMenuRunning = False
                        playScreenRunning = True
                        initiateScreen = True
                    
                    #Help
                    elif (screenDimensions[0]- 225)//2 + 225 > mouse_x > (screenDimensions[0]- 225)//2 and 5.7*screenDimensions[1]/10 + 70 > mouse_y > 5.7*screenDimensions[1]/10:
                        print("HELP")
                    
                    #Quit
                    if (screenDimensions[0]- 330)//2 + 330 > mouse_x > (screenDimensions[0]- 330)//2 and 6.6*screenDimensions[1]/10 + 90 > mouse_y > 6.6*screenDimensions[1]/10:
                        quitGame()


                elif pauseMenuRunning:
                    #Resume
                    if (screenDimensions[0]- 400)//2 + 400 > mouse_x > (screenDimensions[0]- 400)//2 and 3.5*screenDimensions[1]/10 + 90 > mouse_y > 3.5*screenDimensions[1]/10:
                        # play()
                        pauseMenuRunning = False
                        playScreenRunning = True
                        initiateScreen = True

                    
                    #Help
                    elif (screenDimensions[0]- 375)//2 + 375 > mouse_x > (screenDimensions[0]- 375)//2 and 5*screenDimensions[1]/10 + 90 > mouse_y > 5*screenDimensions[1]/10:
                        print("HELP")
                    
                    #Quit
                    if (screenDimensions[0]- 330)//2 + 330 > mouse_x > (screenDimensions[0]- 330)//2 and 6.6*screenDimensions[1]/10 + 90 > mouse_y > 6.6*screenDimensions[1]/10:
                        quitGame()
                
                
                # elif helpMenuRunning:
                #     #Resume
                #     if (screenDimensions[0]- 400)//2 + 400 > mouse_x > (screenDimensions[0]- 400)//2 and 3.5*screenDimensions[1]/10 + 90 > mouse_y > 3.5*screenDimensions[1]/10:
                #         play()
                    
                #     #Help
                #     elif (screenDimensions[0]- 375)//2 + 375 > mouse_x > (screenDimensions[0]- 375)//2 and 5*screenDimensions[1]/10 + 90 > mouse_y > 5*screenDimensions[1]/10:
                #         print("HELP")
                    
                #     #Quit
                #     if (screenDimensions[0]- 330)//2 + 330 > mouse_x > (screenDimensions[0]- 330)//2 and 6.6*screenDimensions[1]/10 + 90 > mouse_y > 6.6*screenDimensions[1]/10:
                #         quitGame()

                elif playScreenRunning:

                    # globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth - 50, 58, 50, 50)

                    if  globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth > mouse_x >  globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth - 50 and 58+50 > mouse_y > 50:
                        print("HI")
                        initiateScreen = True
                        playScreenRunning = False
                        pauseMenuRunning = True

                    if removeVertical == False and removeHorizontal == False and shiftItemsDown == False:
                            itemSelected = True
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
                            
                                if len(displayedArray) == 0:                 
                                    selectedArray.append([columnLocation, rowLocation])
                                    #Selected array and displayedArray -> moves from selected to displayed

                                    selectedItem = True
                                    addItemBorder = True


                                elif len(displayedArray) == 1:
                                    # There is 1 item currently selected
                                    swappedItems = False
                                    swappedBoard = copy.deepcopy(board)
                                    
                                    # The player selects the same position (row and column) twice
                                    if displayedArray[0][0] == columnLocation and displayedArray[0][1] == rowLocation:
                                        removeItemBorder = True

                                    #Two items are identical in a column (vertical)
                                    elif displayedArray[0][0] == columnLocation and displayedArray[0][1] == rowLocation+1:
                                        swappedItems = True
                                        swappedBoard[columnLocation][rowLocation], swappedBoard[columnLocation][rowLocation+1] = swappedBoard[columnLocation][rowLocation+1], swappedBoard[columnLocation][rowLocation]

                                    elif displayedArray[0][0] == columnLocation and displayedArray[0][1] == rowLocation-1:
                                        swappedItems = True
                                        swappedBoard[columnLocation][rowLocation], swappedBoard[columnLocation][rowLocation-1] = swappedBoard[columnLocation][rowLocation-1], swappedBoard[columnLocation][rowLocation]
                                    
                                    #Two items are identical in a row (horizontal)
                                    elif displayedArray[0][1] == rowLocation and displayedArray[0][0] == columnLocation+1:
                                        swappedItems = True
                                        swappedBoard[columnLocation][rowLocation], swappedBoard[columnLocation+1][rowLocation] = swappedBoard[columnLocation+1][rowLocation], swappedBoard[columnLocation][rowLocation]
                                    
                                    elif displayedArray[0][1] == rowLocation and displayedArray[0][0] == columnLocation-1:
                                        swappedItems = True
                                        swappedBoard[columnLocation][rowLocation], swappedBoard[columnLocation-1][rowLocation] = swappedBoard[columnLocation-1][rowLocation], swappedBoard[columnLocation][rowLocation]
                                    
                                    else:
                                        selectedArray.append([columnLocation, rowLocation])
                                        addItemBorder = True

                                        removeItemBorder = True
                                        #Remove it from the PREVIOUS one

                                    # If one of the 'swapped' conditions has been met
                                    if swappedItems == True:
                                        verticalCollectedSwapped = itemCollectVertical(swappedBoard, itemTypes)
                                        horizontalCollectedSwapped = itemCollectHorizontal(swappedBoard, itemTypes)
                                        if len(verticalCollectedSwapped) > 0 or len(horizontalCollectedSwapped) > 0:
                                            gameChanged = True

                                            drawGridItem(board[displayedArray[0][0]][displayedArray[0][1]], rowLocation, columnLocation, itemSize, 0)
                                            drawGridItem(board[columnLocation][rowLocation], displayedArray[0][1], displayedArray[0][0], itemSize, 0)
                                            boardChanged = True

                                            board = copy.deepcopy(swappedBoard)
                                            selectedArray = []
                                            displayedArray = []

                                            

                                            if startLevel == False:
                                                modifyEnergy = -0.25

                                            # print('MAKING BOARD AGAIN')
                                        
                                        elif swappedBoard[displayedArray[0][0]][displayedArray[0][1]] == board[displayedArray[0][0]][displayedArray[0][1]]:
                                            removeItemBorder = True
                                            selectedArray = []
                                            
                                            if startLevel == False:
                                                modifyEnergy = -0.5

                                        # The items are not swapped
                                        else:
                                            removeItemBorder = True
                                            selectedArray = []
                                            if startLevel == False:
                                                modifyEnergy = -0.5

    clock.tick(FPS)

pygame.quit()