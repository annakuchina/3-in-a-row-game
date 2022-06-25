import os, pygame, random, sys, math
from re import T

import globs
import copy
from gameFunctions import itemCollectHorizontal, itemCollectVertical, shiftDown

clock = pygame.time.Clock()
FPS = 8

pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()
SCREEN = pygame.display.set_mode((925, 840))
pygame_icon = pygame.image.load(os.path.join("images", "mushroomScaled" + ".png")).convert_alpha()
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('Woodland')

pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN])

itemTypes = globs.itemTypes
itemLen = globs.itemLen
itemsDrawn = False

pygame.mixer.music.load(os.path.join("files", "backgroundMusic.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)  # Loop music forever


clickSound = pygame.mixer.Sound(os.path.join("files", "click.mp3"))
itemDisappearSound =  pygame.mixer.Sound(os.path.join("files", "itemDisappear.mp3"))
dropDownSound = pygame.mixer.Sound(os.path.join("files", "dropDown.mp3"))


SQUARESIZE = 8
width = globs.COLUMN_COUNT * SQUARESIZE
height = (globs.ROW_COUNT+1) * SQUARESIZE
size = (width, height)
board = {}
unmovedBoard = {}
fullPlayerStatsList = []
levelNumber = 1
gameChanged = False
gameOver = False
selectedArray = []
removeHorizontalCurrent = False
removeVerticalCurrent = False
removalAction = False
last_pos = (0, 0)
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
previousRemoveVerticalCount = -1
previousRemoveHorizontalCount = -1

# Different screens
previousScreen = ""
gameRunning = True
initiateScreen = True
firstRound = True
startLevel = True

mainMenuRunning = True
pauseMenuRunning = False
helpMenuRunning = False
playScreenRunning = False
levelUpScreenRunning = False
loseScreenRunning = False
winScreenRunning = False

shiftItemsDown = False
screenDimensions = [925, 840] 

# Colors
whiteColor = (255, 255, 255)
blackColor = (0, 0, 0)
backgroundPeachColor = (247, 187, 150)
darkerOrangeColor = (255, 155, 68)
lighterOrangeColor = (255, 174, 99)
brighterOrangeColor = (255, 151, 48)
orangeRedColor = (244, 121, 44)
blueColor = (88, 102, 229)
redColor = (226, 39, 38)
pinkColor = (216, 30, 92)
lighterPinkColor = (242, 50, 111)
purpleColor = (189, 99, 217)
brighterPurpleColor = (201, 86, 239)

mushroomSimpleColor = (241, 60, 62)
treeSimpleColor = (246, 107, 47)

image = ""
allSprites = pygame.sprite.Group()
itemSize = [72, 72]

innerSpacing = 8
outerTopMargin = 155
outerLeftMargin = 50
sidebarLeftSpacing = 30
sideBarWidth = 155

deleteAnimation = ["BLANKDynamic", "BLANK"]
spacingAnimation = [0, 0.33333333, 0.66666666, 1]

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
        self.blankSidebar = pygame.image.load(os.path.join("images", "BLANKSidebar.png")).convert()
        self.blankDynamic = pygame.image.load(os.path.join("images", "BLANKDynamic.png")).convert_alpha()

        self.matchPreview = pygame.image.load(os.path.join("images", "matchPreview.png")).convert()
        
        global itemDict
        global mushroomSimpleColor, treeSimpleColor
        global playerStats
        global itemCountDict
        global levelInfoDict

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
        "BLANKSidebar": self.blankSidebar,
        "BLANKDynamic": self.blankDynamic,

        "matchPreview": self.matchPreview
        }
        
        playerStats = {
            # 0 index: order in which the item is in display, 1: the previous count of items, 2: the current count of items
            "heart": [0, 3, 3],
            "energy": [1, 3, 3],

             # 0: the previous count of items (total), 1: the current added count of items
            "tree": [0, 0],
            "mushroom": [0, 0]
        }
        
        # 0 index: order in which the item is display, 1: the previous count of items, 2: the current count of items, 3: the required tally of items, 4: the colour corresponding to the item
        itemCountDict = {
            "mushroomSimple": [0, 0, 0, 0, mushroomSimpleColor],
            "treeSimple": [1, 0, 0, 0, treeSimpleColor],
            "moonSimple": [2, 0, 0, 0, (175, 72, 238)],
            "healPotionSimple": [3, 0, 0, 0, (202, 18, 81)],
            "snakeSimple": [4, 0, 0, 0, (88, 102, 229)],
            "poisonPotionSimple": [5, 0, 0, 0, (15, 130, 85)]
        }

        # How many items are required to collect (by level number)
        levelInfoDict = {
            "mushroomSimple": [4, 5, 6, 7, 8],
            "treeSimple": [6, 7, 8, 9, 10],
            "moonSimple": [8, 8, 9, 10, 11],
            "healPotionSimple": [5, 8, 9, 10, 11],
            "snakeSimple": [7, 6, 5, 4, 4],
            "poisonPotionSimple": [8, 7, 6, 5, 4]
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

# Board, grid drawing functions
def drawGridItem(chosenItem, rowNo, colNo, givenItemSize, rowMultiplier):
    xLocation = colNo*givenItemSize[0] + innerSpacing*colNo + outerLeftMargin
    yLocation = (rowNo+rowMultiplier)*givenItemSize[1] + innerSpacing*(rowNo+rowMultiplier) + outerTopMargin
    width = givenItemSize[0]
    height = givenItemSize[1]
    scene = Item()
    scene.drawItem(chosenItem, xLocation, yLocation, width, height)

def makeBoard(givenBoard):
    for c, colArray in givenBoard.items():
        r = 0
        for chosenItem in colArray:
            drawGridItem(chosenItem, r, c, itemSize, 0)
            r+=1

def randomBoard():
    for c in range(globs.COLUMN_COUNT):
        colArray = []
        for r in range(globs.ROW_COUNT):
            chosenItem = itemTypes[random.randint(0, globs.itemLen-1)]
            colArray.append(chosenItem)
            drawGridItem(chosenItem, r, c, itemSize, 0)
        
        board[c] = colArray
    return board

# Generate the board randomly
randomBoard()


def drawCenterText(displayText, textSize, textColor, xBackgroundWidth, yLocation):
    font = pygame.font.Font(os.path.join("files","prstartk.ttf"), textSize)
    textSurface = font.render(displayText, False, textColor)
    textRect = textSurface.get_rect(center = (xBackgroundWidth, yLocation))
    SCREEN.blit(textSurface, textRect)

def drawText(displayText, textSize, textColor, xLocation, yLocation):
    font = pygame.font.Font(os.path.join("files","prstartk.ttf"), textSize)
    textSurface = font.render(displayText, False, textColor)
    SCREEN.blit(textSurface, (xLocation, yLocation))

def button(textContent, xLocation, yLocation, width, height, backgroundColor, textColor, textSize):
    pygame.draw.rect(SCREEN, backgroundColor, (xLocation, yLocation, width, height))
    drawCenterText(textContent, textSize, textColor, width//2 + xLocation, height//2 + yLocation)


# START of the play screen drawing functions
def drawItemCount(item):
    global itemsDrawn
    itemCountMessage = str(itemCountDict[item][1]) + "/" + str(itemCountDict[item][3])
    xTextLocation = outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + 67
    yTextLocation = itemCountDict[item][0]*55 + 2.5*itemSize[1] + outerTopMargin - 16 + 25
    
    textColor = ""

    # Add a different color if it is full
    if itemCountDict[item][2] == itemCountDict[item][3]:
        textColor = itemCountDict[item][4]

    if itemCountDict[item][0] > 1:
        yTextLocation += 55
    
    if itemCountDict[item][0] > 3:
        yTextLocation += 35
        if textColor == "":
            textColor = blackColor
    else:
        if textColor == "":
            textColor = whiteColor

    # If icons have already been drawn, cover over them with the background color to clear them
    if itemsDrawn == True:
        drawText(itemCountMessage, 16, lighterOrangeColor, xTextLocation, yTextLocation)
        itemCountMessage = str(itemCountDict[item][2]) + "/" + str(itemCountDict[item][3])
    
    drawText(itemCountMessage, 16, textColor, xTextLocation, yTextLocation)
    itemsDrawn = True

def calculatePlayerStats(item, itemNumber):
    global fullPlayerStatsList

    # User reached the required amount of items
    if itemCountDict[item][2] + itemNumber >= itemCountDict[item][3]:
        itemCountDict[item][1] = itemCountDict[item][2]
        itemCountDict[item][2] = itemCountDict[item][3]
        fullPlayerStatsList.append(item)
        drawItemCount(item)
    
     # User has not reached the required amount of items yet
    elif itemCountDict[item][2] != itemCountDict[item][3]:
        itemCountDict[item][1] = itemCountDict[item][2]
        itemCountDict[item][2] += itemNumber
        drawItemCount(item)

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

        if count > 3:
            yLocation += 35

        #Friendlies
        if count == 0:
            drawText("+", 60, darkerOrangeColor, xLocation + 22, yLocation - 50)
            drawText("+", 40, whiteColor, xLocation + 32, yLocation - 41)
        
        #Enemies
        elif count == 4:
            drawText("x", 56, darkerOrangeColor, xLocation + 22 + 3 + 4, yLocation - 49 - 3)
            drawText("x", 40, blackColor, xLocation + 32 + 4, yLocation - 41 - 3 + 1)

        scene.drawItem(item, xLocation, yLocation, width, height)
        drawItemCount(item)
    scene = Item()
    scene.drawItem("collectionBorderRed", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing +25, 2*55 + 2.5*itemSize[1] + outerTopMargin - 7, 45, 45)
    scene = Item()
    scene.drawItem("collectionBorderOrange", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + (sideBarWidth - 45) - 25, 2*55 + 2.5*itemSize[1] + outerTopMargin - 7, 45, 45)
    allSprites.draw(SCREEN)

# Draw the energy and heart icons
def drawPlayerStats(item, itemNumber):
    playerStats[item][1] = playerStats[item][2]
    playerStats[item][2] += itemNumber

    selectedItem = item

    # There are less items there than there were previously, clear the player statistics
    if playerStats[item][2] < playerStats[item][1]:
        xLocation = outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + 20 + sidebarLeftSpacing
        yLocation = 2*itemSize[0]/3 + outerTopMargin + playerStats[item][0]*40
        width = 3*30 + 2*10
        height = 30
        scene = Item()
        scene.drawItem("BLANKSidebar", xLocation, yLocation, width, height)

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
    allSprites.draw(SCREEN)

# Filling the tree and mushroom collection meters
def fillCollection(item):
    xLocation = outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + 6 + 25
    yLocation = 42 + 2*55 + 2.5*itemSize[1] + outerTopMargin - 7

    if playerStats[item][0] + playerStats[item][1] >= 12:
        playerStats[item][1] = 12 - playerStats[item][0]

    # There were items in the collection that were not displayed
    if playerStats[item][0] > 0 and playerStats[item][1] == 0:
        playerStats[item][1] = playerStats[item][0]
        playerStats[item][0] = 0

    currentFillStatus = playerStats[item][1] * 3
    previousFillStatus = playerStats[item][0] * 3

    if item == "mushroom":
        selectedColor = mushroomSimpleColor

    elif item == "tree":
        selectedColor = treeSimpleColor
        xLocation = xLocation + sideBarWidth - 45 - 50

    # If it previously wasn't filled at all, fill in the first one
    if playerStats[item][0] == 0 and playerStats[item][1] > 0 or playerStats[item][0] > 1 and initiateScreen == True:
        collectionBg = pygame.Rect(xLocation + 3, yLocation - 3, 45 - 12 - 6, 3)
        pygame.draw.rect(SCREEN, selectedColor, collectionBg)


        if playerStats[item][1] > 1:
            collectionBg = pygame.Rect(xLocation, yLocation - currentFillStatus, 45 - 12, currentFillStatus - 3)
            pygame.draw.rect(SCREEN, selectedColor, collectionBg)

    else:
        collectionBg = pygame.Rect(xLocation, yLocation - currentFillStatus - previousFillStatus, 45 - 12, currentFillStatus)
        pygame.draw.rect(SCREEN, selectedColor, collectionBg)

    playerStats[item][0] += playerStats[item][1]
    playerStats[item][1] = 0

def drawLevel():
    for item in levelInfoDict:
        itemCountDict[item][3] = levelInfoDict[item][levelNumber-1]
        
    if levelNumber > 1:
        drawText("L" + str(levelNumber), 40, darkerOrangeColor, outerLeftMargin+50, 62)
    drawText("L" + str(levelNumber), 40, whiteColor, outerLeftMargin+50, 62)

def drawSidebar():
    #Draw the orange background
    rect_object = pygame.Rect(0, 0, screenDimensions[0], screenDimensions[1])
    pygame.draw.rect(SCREEN, backgroundPeachColor, rect_object)

    #Draw the top bar
    topBarBg = pygame.Rect(outerLeftMargin, 35, globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth, 90)
    pygame.draw.rect(SCREEN, whiteColor, topBarBg)
    topBar = pygame.Rect(outerLeftMargin+5, 40, globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth - 10, 80)
    pygame.draw.rect(SCREEN, darkerOrangeColor, topBar)

    #Draw the right side bar
    sideBarBg = pygame.Rect(outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing)+ sidebarLeftSpacing, outerTopMargin, sideBarWidth, (itemSize[1])*globs.COLUMN_COUNT + innerSpacing*(globs.COLUMN_COUNT-1))
    pygame.draw.rect(SCREEN, whiteColor, sideBarBg)
    sideBar = pygame.Rect(outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing)+sidebarLeftSpacing+5, outerTopMargin+5, sideBarWidth-10, (itemSize[1])*globs.COLUMN_COUNT + innerSpacing*(globs.COLUMN_COUNT-1)-10)
    pygame.draw.rect(SCREEN, lighterOrangeColor, sideBar)

    textMessage = "Woodland"
    drawCenterText(textMessage, 50, pinkColor, screenDimensions[0]/2 + 4 + 5, outerTopMargin/2 + 6)
    drawCenterText(textMessage, 50, whiteColor, screenDimensions[0]/2 + 5, outerTopMargin/2 + 6)

    drawLevel()

    scene = Item()
    scene.drawItem("pauseButton", outerLeftMargin + globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth/3 + 5, 58, 50, 50)


def levelUp():
    allSprites.empty()

    levelUpBg = pygame.Rect(itemSize[0] + innerSpacing + outerLeftMargin, 2*itemSize[0] + innerSpacing*2 + outerTopMargin, itemSize[0]*6 + innerSpacing*5, itemSize[0]*4 + innerSpacing*3)
    pygame.draw.rect(SCREEN, whiteColor, levelUpBg)

    drawCenterText("Level Up!", 40, treeSimpleColor, (itemSize[0] + innerSpacing + outerLeftMargin) + (itemSize[0]*6 + innerSpacing*5)/2, 3.3*itemSize[0] + innerSpacing*3 + outerTopMargin)
    
    button("Continue", outerLeftMargin + 2.5*itemSize[0] + 2*innerSpacing, 4*itemSize[0] + innerSpacing*3 + outerTopMargin, 3*itemSize[0] + 3*innerSpacing, 90, mushroomSimpleColor, whiteColor, 20)
# END of screen drawing functions


# Start of drawing the other screens
def play(): 
    allSprites.empty()
    makeBoard(board)
    drawSidebar()
    drawPlayerStats("heart", 0)
    drawPlayerStats("energy", 0)
    drawSidebarIcons()
    fillCollection("mushroom")
    fillCollection("tree")

def quitGame():
    pygame.quit()
    quit()

def pauseMenu():
    allSprites.empty()
    SCREEN.fill(backgroundPeachColor)
    screenTitle = "Pause"
    drawCenterText(screenTitle, 80, whiteColor, screenDimensions[0]//2, 2.7*screenDimensions[1]/10)
    button("Resume", (screenDimensions[0]- 400)//2, 3.5*screenDimensions[1]/10, 400, 90, whiteColor, lighterPinkColor, 30)
    button("Help", (screenDimensions[0]- 375)//2, 5*screenDimensions[1]/10, 375, 90, whiteColor, brighterOrangeColor, 30)
    button("Quit", (screenDimensions[0]- 330)//2, 6.6*screenDimensions[1]/10, 330, 90, whiteColor, brighterPurpleColor, 30)

def winScreen():
    allSprites.empty()
    SCREEN.fill(darkerOrangeColor)
    drawCenterText("You Win!", 70, whiteColor, screenDimensions[0]//2, 2.7*screenDimensions[1]/10)
    button("Main Menu", (screenDimensions[0]- 375)//2, 3.5*screenDimensions[1]/10, 375, 90, whiteColor, lighterPinkColor, 26)
    button("Help", (screenDimensions[0]- 350)//2, 5*screenDimensions[1]/10, 350, 90, whiteColor, brighterOrangeColor, 26)
    button("Quit", (screenDimensions[0]- 325)//2, 6.5*screenDimensions[1]/10, 325, 90, whiteColor, brighterPurpleColor, 26)

def loseScreen():
    allSprites.empty()
    SCREEN.fill(blueColor)
    drawCenterText("You Lose!", 70, whiteColor, screenDimensions[0]//2, 2.7*screenDimensions[1]/10)
    button("Main Menu", (screenDimensions[0]- 375)//2, 3.5*screenDimensions[1]/10, 375, 90, whiteColor, lighterPinkColor, 26)
    button("Help", (screenDimensions[0]- 350)//2, 5*screenDimensions[1]/10, 350, 90, whiteColor, brighterOrangeColor, 26)
    button("Quit", (screenDimensions[0]- 325)//2, 6.5*screenDimensions[1]/10, 325, 90, whiteColor, brighterPurpleColor, 26)

def helpMenu():
    allSprites.empty()
    SCREEN.fill(whiteColor)

    rectObject = pygame.Rect(0, 0, screenDimensions[0], screenDimensions[1])
    pygame.draw.rect(SCREEN, lighterOrangeColor, rectObject)
    rectObject = pygame.Rect(20, 20, screenDimensions[0]-40, screenDimensions[1]-40)
    pygame.draw.rect(SCREEN, whiteColor, rectObject)
    topMargin = 77
    drawCenterText("Help", 55, orangeRedColor, screenDimensions[0]//2, 1*screenDimensions[1]/10)

    line1 = "To swap/collect items, click two adjacent items."
    line2 = "They must create a 3+ in a row/column when swapped."

    line3 = "Fill the collections with friendly items to level up!"
    line4 = "Collecting friendly items also restores health/energy: "
    line5 = "Mushrooms, trees, moons, healing potions"

    line6 = "Beware of enemies! Snakes will drain your health."
    line7 = "Poison potions will deplete both energy and health."

    line8 = "The item board shuffles before each round."
    line9 = "Pass five levels to win!"

    textDict = {0: [line1, line2], 1: [line3, line4, line5], 2: [line6, line7], 3:[line8, line9]}

    imagePadding = 0

    goodItems = ["mushroom", "tree", "healPotion", "moon"]
    badItems = ["snake", "poisonPotion"]
    textColor = orangeRedColor

    spaceCount = 0
    for key in textDict: # Each paragraph
        spaceCount += 0.5
        for line in textDict[key]:
            spaceCount += 0.3
            drawCenterText(line, 15, textColor, screenDimensions[0]//2, spaceCount*screenDimensions[1]/10 + topMargin + imagePadding)

        if key == 0:
            textColor = pinkColor
            scene = Item()
            scene.drawItem("matchPreview", screenDimensions[0]//2 - 336/2, spaceCount*screenDimensions[1]/10 + topMargin + 15, 336, 84)
            imagePadding += 84 - 22

        if key == 1:
            textColor = blueColor
            itemCount = 0
            for item in goodItems:
                
                scene = Item()
                scene.drawItem(item, screenDimensions[0]//2 - 80*(len(goodItems))//2 + (itemCount)*80, spaceCount*screenDimensions[1]/10 + topMargin + imagePadding + 15, 80, 80)
                itemCount += 1
            imagePadding += 80 - 22
        
        if key == 2:
            textColor = orangeRedColor
            itemCount = 0
            for item in badItems:
                itemCount += 1
                scene = Item()
                scene.drawItem(item, screenDimensions[0]//2 - 80*len(badItems) + (itemCount)*80, spaceCount*screenDimensions[1]/10 + topMargin + imagePadding + 15, 80, 80)
            imagePadding += 80 - 22

    button("Back", (screenDimensions[0]- 250)//2, 8.2*screenDimensions[1]/10, 250, 70, redColor, whiteColor, 25)

    pygame.display.update()
    allSprites.draw(SCREEN)
    

def mainMenu():
    allSprites.empty()
    rectObject = pygame.Rect(0, 0, screenDimensions[0], screenDimensions[1])
    pygame.draw.rect(SCREEN, darkerOrangeColor, rectObject)
    rectObject = pygame.Rect(40, 40, screenDimensions[0]-80, screenDimensions[1]-80)
    pygame.draw.rect(SCREEN, whiteColor, rectObject)
    drawCenterText("Woodland", 80, redColor, screenDimensions[0]//2, 3.5*screenDimensions[1]/10)
    scene = Item()
    scene.drawItem("mushroomTransparent", 2*screenDimensions[0]/10, 1.4*screenDimensions[1]/10, 150, 150)
    scene = Item()
    scene.drawItem("treeTransparent", 7*screenDimensions[0]/10, 3.9*screenDimensions[1]/10, 150, 150)
    button("Start", (screenDimensions[0]- 250)//2, 4.5*screenDimensions[1]/10, 250, 70, lighterPinkColor, whiteColor, 25)
    button("Help", (screenDimensions[0]- 225)//2, 5.7*screenDimensions[1]/10, 225, 70, darkerOrangeColor, whiteColor, 25)
    button("Quit", (screenDimensions[0]- 200)//2, 7*screenDimensions[1]/10, 200, 70, purpleColor, whiteColor, 25)

    allSprites.draw(SCREEN)
# End of drawing the other screens


def redrawGameWindow():
    global verticalRemoveCount, horizontalRemoveCount
    global removeVerticalCurrent, removeHorizontalCurrent
    global itemsModified
    global shiftDownCount
    global shiftItemsDown
    global addItemBorder, removeItemBorder
    global selectedArray, displayedArray
    global boardChanged
    global startLevel
    global fullPlayerStatsList
    global modifyHearts, modifyEnergy
    global levelUpScreenRunning, initiateScreen, playScreenRunning, loseScreenRunning
    global previousRemoveVerticalCount, previousRemoveHorizontalCount

    if verticalRemoveCount + 1 >= 5:
        # 4 total frames
        verticalRemoveCount = 0
        removeVerticalCurrent = False

    if horizontalRemoveCount + 1 >= 5:
        horizontalRemoveCount = 0
        removeHorizontalCurrent = False

    if shiftDownCount + 1 >= 5:
        # 4 total frames
        shiftDownCount = 0
        shiftItemsDown = False

    if removeVerticalCurrent:
        if previousRemoveVerticalCount != verticalRemoveCount//2:
            for key in verticalDict:
                for item in verticalDict[key]:
                    if isinstance(item, list):
                        for rowNo in item:
                            drawGridItem(deleteAnimation[verticalRemoveCount//2], rowNo, key, itemSize, 0)
                            boardChanged = True

        previousRemoveVerticalCount = verticalRemoveCount
        verticalRemoveCount += 1
        
    if removeHorizontalCurrent:
        if previousRemoveHorizontalCount != horizontalRemoveCount//2:
            for key in horizontalDict:
                for item in horizontalDict[key]:
                    if isinstance(item, list):
                        for colNo in item:
                            drawGridItem(deleteAnimation[horizontalRemoveCount//2], key, colNo, itemSize, 0)
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
            
            # The blank spaces in between the unmoved rows are drawn, and then the items are drawn
            drawGridItem("BLANK", 0, key, [itemSize[1], unmovedRow*itemSize[0] + (unmovedRow-1)*innerSpacing], 0)
            for movedItem in movedItemsBoard[key]:
                selectedItem = board[key][movedItem]
                if movedItem == 0:
                    if "BLANK" not in board[key] and shiftDownCount==3: 
                        drawGridItem(selectedItem, movedItem, key, itemSize, 0)
                        itemsModified = True
                        # Switching the item above for the one below
                else:
                        drawGridItem(selectedItem, movedItem-1, key, itemSize, spacingAnimation[shiftDownCount//1])
                        itemsModified = True
        shiftDownCount += 1

    if removeItemBorder:
        drawGridItem("deselectedOutline", displayedArray[0][1], displayedArray[0][0], itemSize, 0)
        displayedArray = []
        removeItemBorder = False
        boardChanged = True

    if addItemBorder:
        drawGridItem("selectedOutline", selectedArray[0][1], selectedArray[0][0], itemSize, 0)
        startLevel = False
        addItemBorder = False
        displayedArray = selectedArray
        selectedArray = []
        boardChanged = True

    if modifyEnergy != 0:
        if playerStats["energy"][2] + modifyEnergy <= 0:
            initiateScreen = True
            playScreenRunning = False
            loseScreenRunning = True
        else:
            drawPlayerStats("energy", modifyEnergy)
            modifyEnergy = 0
            boardChanged = True


    if len(fullPlayerStatsList) > 0 and gameChanged == True and firstRound == False:
        # Do different actions according to the filled items
        for item in fullPlayerStatsList:

            # Friendly items
            if item == "mushroomSimple":
                modifyHearts = 0.5
                playerStats["mushroom"][1] += 3

            elif item == "treeSimple":
                modifyEnergy = 0.5
                playerStats["tree"][1] += 3

            elif item == "healPotionSimple":
                modifyEnergy = 2
                modifyHearts = 2
                
                # Already have maximum health available
                if playerStats["heart"][2] == 3:
                    playerStats["mushroom"][1] += 1
                    playerStats["tree"][1] += 1

                # Already have maximum energy available
                if playerStats["energy"][2] == 3:
                    playerStats["mushroom"][1] += 1
                    playerStats["tree"][1] += 1

            elif item == "moonSimple":
                playerStats["mushroom"][1] += 1
                playerStats["tree"][1] += 1

            # Enemy items
            elif item == "snakeSimple":
                modifyHearts = -0.5

            elif item == "poisonPotionSimple":
                modifyEnergy = -0.5
                modifyHearts = -0.5

            # Tree, mushroom collections being filled
            if playerStats["tree"][1] > 0:
                if playerStats["tree"][0] > 12:
                    playerStats["mushroom"][1] += playerStats["tree"][0]
                else:
                    fillCollection("tree")

            if playerStats["mushroom"][1] > 0:
                if playerStats["mushroom"][0] > 12:
                    playerStats["tree"][1] += playerStats["mushroom"][0]
                else:
                    fillCollection("mushroom")

            if playerStats["mushroom"][0] == 12 and playerStats["tree"][0] == 12:
                levelUpScreenRunning = True
                playScreenRunning = False
                initiateScreen = True

            if modifyEnergy > 0:
                if modifyEnergy + playerStats["energy"][2] >= 3:
                    drawPlayerStats("energy", 3 - playerStats["energy"][2])
                else:
                    drawPlayerStats("energy", modifyEnergy)

            elif modifyEnergy < 0:
                # modifyEnergy takes away more energy than is available (player loses)
                if -modifyEnergy >= playerStats["energy"][2]:
                    initiateScreen = True
                    playScreenRunning = False
                    loseScreenRunning = True
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
                    initiateScreen = True
                    playScreenRunning = False
                    loseScreenRunning = True
                else:
                    drawPlayerStats("heart", modifyHearts)

            modifyEnergy = 0
            modifyHearts = 0

            # Updating the previous and current itemCountDict items
            itemCountDict[item][1] = itemCountDict[item][2]
            itemCountDict[item][2] = 0
            drawItemCount(item)

        fullPlayerStatsList = []
        boardChanged = True  

    # If something on the board has been modified, draw it to the screen
    if boardChanged:
        allSprites.draw(SCREEN)
        pygame.display.update()
        boardChanged = False


while gameRunning:
    # Get mouse position with each clock tick
    mouse_pos = pygame.mouse.get_pos()
    if (mouse_pos != last_pos):
        mouse_x, mouse_y = mouse_pos
        last_pos = mouse_pos

    if playScreenRunning:
        if initiateScreen:
            play()
            # Checking if player statistics are full
            if playerStats["tree"][0] == 12 and playerStats["mushroom"][0] == 12:
                playScreenRunning = False
                levelUpScreenRunning = True
                initiateScreen = True

            else:
                play()
                pygame.display.update()
                initiateScreen = False
                firstRound = True
                gameChanged = True

        # If the game is changed, check if there are vertical and horizontal matches, and then update them to disappear
        if gameChanged == True and shiftItemsDown == False:
            verticalDict = itemCollectVertical(board, itemTypes)
            horizontalDict = itemCollectHorizontal(board, itemTypes)

            if len(verticalDict) > 0:
                removeVerticalCurrent = True
                removalAction = True
                pygame.mixer.Channel(1).play(itemDisappearSound)
            
                for key in verticalDict:
                    for item in verticalDict[key]:
                        if isinstance(item, list):
                            # Check that it's not 3 blank's in a row
                                matchItem = board[key][item[0]]
                                matchLength = len(item)
                                if startLevel == False:
                                    if matchItem != "BLANK" and firstRound == False:
                                        calculatePlayerStats(matchItem + "Simple", matchLength)
                                for rowNo in item:
                                    board[key][rowNo] = "BLANK"

            else:
                removeVerticalCurrent = False
                removeCount = 0
                verticalRemoveCount = 0

            if len(horizontalDict) > 0:
                removeHorizontalCurrent = True
                removalAction = True
                pygame.mixer.Channel(1).play(itemDisappearSound)

                for key in horizontalDict:
                    for item in horizontalDict[key]:
                        if isinstance(item, list):
                                matchItem = board[item[0]][key]
                                matchLength = len(item)
                                if startLevel == False:
                                    if matchItem != "BLANK" and firstRound == False:
                                        calculatePlayerStats(matchItem + "Simple", matchLength)
                                for colNo in item:
                                    board[colNo][key] = "BLANK"

            else:
                removeHorizontalCurrent = False
                removeCount = 0
                horizontalRemoveCount = 0

            gameChanged = False
        
        # Move columns down if items have been removed
        if removeVerticalCurrent == False and removeHorizontalCurrent == False and shiftItemsDown == False and removalAction == True:
            unmovedBoard = {}
            movedItemsBoard = {}

            for key in board:
                if "BLANK" in board[key]:
                    shiftItemsDown = True
                    pygame.mixer.Channel(2).play(dropDownSound)
                    modifiedItems, unchangedCol, shiftedCol = shiftDown(board[key])
                    movedItemsBoard[key] = modifiedItems
                    board[key] = shiftedCol
                    unmovedBoard[key] = unchangedCol
                    
            if shiftItemsDown == False:
                removalAction = False

        if itemsModified == True and shiftItemsDown == False:
            gameChanged = True
            itemsModified = False
        redrawGameWindow()

    elif mainMenuRunning:
        if initiateScreen:
            mainMenu()
            pygame.display.update()
            initiateScreen = False

    elif levelUpScreenRunning:
        if initiateScreen:
            levelUp()

            pygame.display.update()
            initiateScreen = False

    elif winScreenRunning:
        if initiateScreen:
            modifyEnergy = 0
            modifyHearts = 0

            board = {}
            levelNumber = 1
            playerStats = {
            "heart": [0, 3, 3],
            "energy": [1, 3, 3],
            "tree": [0, 0],
            "mushroom": [0, 0]
            }

            itemCountDict = {
            "mushroomSimple": [0, 0, 0, 0, mushroomSimpleColor],
            "treeSimple": [1, 0, 0, 0, treeSimpleColor],
            "moonSimple": [2, 0, 0, 0, (175, 72, 238)],
            "healPotionSimple": [3, 0, 0, 0, (202, 18, 81)],
            "snakeSimple": [4, 0, 0, 0, (88, 102, 229)],
            "poisonPotionSimple": [5, 0, 0, 0, (15, 130, 85)]
            }

            randomBoard()
            winScreen()
            pygame.display.update()
            initiateScreen = False
    
    elif loseScreenRunning:
        if initiateScreen:
            modifyEnergy = 0
            modifyHearts = 0

            board = {}
            levelNumber = 1
            playerStats = {
            "heart": [0, 3, 3],
            "energy": [1, 3, 3],
            "tree": [0, 0],
            "mushroom": [0, 0]
            }

            itemCountDict = {
            "mushroomSimple": [0, 0, 0, 0, mushroomSimpleColor],
            "treeSimple": [1, 0, 0, 0, treeSimpleColor],
            "moonSimple": [2, 0, 0, 0, (175, 72, 238)],
            "healPotionSimple": [3, 0, 0, 0, (202, 18, 81)],
            "snakeSimple": [4, 0, 0, 0, (88, 102, 229)],
            "poisonPotionSimple": [5, 0, 0, 0, (15, 130, 85)]
            }

            randomBoard()
            loseScreen()
            pygame.display.update()
            initiateScreen = False

    elif pauseMenuRunning:
        if initiateScreen:
            pauseMenu()
            pygame.display.update()
            initiateScreen = False

    elif helpMenuRunning:
        if initiateScreen:
            helpMenu()
            pygame.display.update()
            initiateScreen = False


    # Check for player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mainMenuRunning:
                    #Play
                    if (screenDimensions[0]- 250)//2 + 250 > mouse_x > (screenDimensions[0]- 250)//2 and 4.5*screenDimensions[1]/10 + 70 > mouse_y > 4.5*screenDimensions[1]/10:
                        pygame.mixer.Channel(0).play(clickSound)
                        mainMenuRunning = False
                        playScreenRunning = True
                        initiateScreen = True
                    
                    #Help
                    elif (screenDimensions[0]- 225)//2 + 225 > mouse_x > (screenDimensions[0]- 225)//2 and 5.7*screenDimensions[1]/10 + 70 > mouse_y > 5.7*screenDimensions[1]/10:
                        pygame.mixer.music.pause()
                        pygame.mixer.Channel(0).play(clickSound)
                        initiateScreen = True
                        previousScreen = "mainMenu"
                        mainMenuRunning = False
                        helpMenuRunning = True

                    #Quit
                    elif (screenDimensions[0]- 330)//2 + 330 > mouse_x > (screenDimensions[0]- 330)//2 and 6.6*screenDimensions[1]/10 + 90 > mouse_y > 6.6*screenDimensions[1]/10:
                        quitGame()

                elif pauseMenuRunning:
                    #Resume
                    if (screenDimensions[0]- 400)//2 + 400 > mouse_x > (screenDimensions[0]- 400)//2 and 3.5*screenDimensions[1]/10 + 90 > mouse_y > 3.5*screenDimensions[1]/10:
                        pygame.mixer.music.unpause()
                        pygame.mixer.Channel(0).play(clickSound)
                        pauseMenuRunning = False
                        playScreenRunning = True
                        initiateScreen = True

                    #Help
                    elif (screenDimensions[0]- 375)//2 + 375 > mouse_x > (screenDimensions[0]- 375)//2 and 5*screenDimensions[1]/10 + 90 > mouse_y > 5*screenDimensions[1]/10:
                        pygame.mixer.Channel(0).play(clickSound)
                        initiateScreen = True
                        previousScreen = "pauseMenu"
                        pauseMenuRunning = False
                        helpMenuRunning = True
                    
                    #Quit
                    if (screenDimensions[0]- 330)//2 + 330 > mouse_x > (screenDimensions[0]- 330)//2 and 6.6*screenDimensions[1]/10 + 90 > mouse_y > 6.6*screenDimensions[1]/10:
                        quitGame()
                
                elif levelUpScreenRunning:
                    # Pause the game
                    if  globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth > mouse_x >  globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth - 50 and 58+50 > mouse_y > 50:
                        pygame.mixer.music.pause()
                        pygame.mixer.Channel(0).play(clickSound)
                        initiateScreen = True
                        levelUpScreenRunning = False
                        pauseMenuRunning = True

                    # Continue
                    if outerLeftMargin + 2.5*itemSize[0] + 2*innerSpacing + 3*itemSize[0] + 3*innerSpacing > mouse_x > outerLeftMargin + 2.5*itemSize[0] + 2*innerSpacing and 4*itemSize[0] + innerSpacing*3 + outerTopMargin + 90 > mouse_y > 4*itemSize[0] + innerSpacing*3 + outerTopMargin:
                        pygame.mixer.Channel(0).play(clickSound)
                        allSprites.empty()
                        boardChanged = True
                        rect_object = pygame.Rect(0, 0, screenDimensions[0], screenDimensions[1])
                        pygame.draw.rect(SCREEN, backgroundPeachColor, rect_object)
                        levelNumber += 1

                        # Win the game
                        if levelNumber == 6:
                            initiateScreen = True
                            levelUpScreenRunning = False
                            winScreenRunning = True
                        else:
                            board = {}
                            modifyEnergy = 0
                            modifyHearts = 0

                            playerStats = {
                            "heart": [0, 3, 3],
                            "energy": [1, 3, 3],
                            "tree": [0, 0],
                            "mushroom": [0, 0]
                            }

                            itemCountDict = {
                            "mushroomSimple": [0, 0, 0, 0, mushroomSimpleColor],
                            "treeSimple": [1, 0, 0, 0, treeSimpleColor],
                            "moonSimple": [2, 0, 0, 0, (175, 72, 238)],
                            "healPotionSimple": [3, 0, 0, 0, (202, 18, 81)],
                            "snakeSimple": [4, 0, 0, 0, (88, 102, 229)],
                            "poisonPotionSimple": [5, 0, 0, 0, (15, 130, 85)]
                            }

                            randomBoard()
                            initiateScreen = True
                            levelUpScreenRunning = False
                            playScreenRunning = True
                            drawLevel()

                elif winScreenRunning:
                    # Main menu
                    if (screenDimensions[0]- 375)//2 + 375 > mouse_x > (screenDimensions[0]- 375)//2 and 3.5*screenDimensions[1]/10 + 90 > mouse_y > 3.5*screenDimensions[1]/10:
                        pygame.mixer.Channel(0).play(clickSound)
                        initiateScreen = True
                        winScreenRunning = False
                        mainMenuRunning = True
                    
                    # Help
                    elif (screenDimensions[0]- 350)//2 + 350 > mouse_x > (screenDimensions[0]- 350)//2 and 5*screenDimensions[1]/10 + 90 > mouse_y > 5*screenDimensions[1]/10:
                        pygame.mixer.music.pause()
                        pygame.mixer.Channel(0).play(clickSound)
                        initiateScreen = True
                        previousScreen = "winScreen"
                        winScreenRunning = False
                        helpMenuRunning = True
                    
                    # Quit
                    elif (screenDimensions[0]- 325)//2 + 325 > mouse_x > (screenDimensions[0]- 325)//2 and 6.5*screenDimensions[1]/10 + 90 > mouse_y > 6.5*screenDimensions[1]/10:
                        winScreenRunning = False
                        quitGame()
                        
                elif loseScreenRunning:
                    # Main menu
                    if (screenDimensions[0]- 375)//2 + 375 > mouse_x > (screenDimensions[0]- 375)//2 and 3.5*screenDimensions[1]/10 + 90 > mouse_y > 3.5*screenDimensions[1]/10:
                        pygame.mixer.Channel(0).play(clickSound)
                        initiateScreen = True
                        loseScreenRunning = False
                        mainMenuRunning = True
                    
                    # Help
                    elif (screenDimensions[0]- 350)//2 + 350 > mouse_x > (screenDimensions[0]- 350)//2 and 5*screenDimensions[1]/10 + 90 > mouse_y > 5*screenDimensions[1]/10:
                        pygame.mixer.music.pause()
                        pygame.mixer.Channel(0).play(clickSound)
                        initiateScreen = True
                        previousScreen = "loseScreen"
                        loseScreenRunning = False
                        helpMenuRunning = True
                    
                    # Quit
                    elif (screenDimensions[0]- 325)//2 + 325 > mouse_x > (screenDimensions[0]- 325)//2 and 6.5*screenDimensions[1]/10 + 90 > mouse_y > 6.5*screenDimensions[1]/10:
                        loseScreenRunning = False
                        quitGame()
                
                elif helpMenuRunning:
                    # Back to previous screen
                    if (screenDimensions[0]- 250)//2 + 250 > mouse_x > (screenDimensions[0]- 250)//2 and 8.2*screenDimensions[1]/10 + 70 > mouse_y > 8.2*screenDimensions[1]/10:
                        pygame.mixer.Channel(0).play(clickSound)
                        initiateScreen = True
                        helpMenuRunning = False

                        if previousScreen == "mainMenu":
                            pygame.mixer.music.unpause()
                            mainMenuRunning = True

                        elif previousScreen == "pauseMenu":
                            pauseMenuRunning = True

                        elif previousScreen == "winScreen":
                            pygame.mixer.music.unpause()
                            winScreenRunning = True

                        elif previousScreen == "loseScreen":
                            pygame.mixer.music.unpause()
                            loseScreenRunning = True

                        previousScreen = ""

                elif playScreenRunning:
                    # Pause the game
                    if  globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth > mouse_x >  globs.COLUMN_COUNT*(itemSize[1]+innerSpacing) + sidebarLeftSpacing + sideBarWidth - 50 and 58+50 > mouse_y > 50:
                        pygame.mixer.music.pause()
                        pygame.mixer.Channel(0).play(clickSound)
                        initiateScreen = True
                        playScreenRunning = False
                        pauseMenuRunning = True

                    if removalAction == False and shiftItemsDown == False:
                        firstRound = False
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
                            pygame.mixer.Channel(0).play(clickSound)
                            verticalDict = itemCollectVertical(board, itemTypes)
                            horizontalDict = itemCollectHorizontal(board, itemTypes)
                        
                            if len(displayedArray) == 0:                 
                                selectedArray.append([columnLocation, rowLocation])
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
                                        # modifyEnergy = -0.25

                                    # The items are not swapped
                                    elif swappedBoard[displayedArray[0][0]][displayedArray[0][1]] == board[displayedArray[0][0]][displayedArray[0][1]]:
                                        removeItemBorder = True
                                        selectedArray = []
                                        modifyEnergy = -0.5

                                    else:
                                        removeItemBorder = True
                                        selectedArray = []
                                        modifyEnergy = -0.5
    clock.tick(FPS)

pygame.quit()