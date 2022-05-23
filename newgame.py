from operator import ne
from optparse import Values
import os, pygame, random, sys, math
from unicodedata import name
import numpy as np
from os import system
import time
import globs
import sampleBoards

# myFont = pygame.font.SysFont("monospace", 60)

ROW_COUNT = 8
COLUMN_COUNT = 8 

FPS = 60
clock = pygame.time.Clock()
pygame.init()

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

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

board = {}


left = 0
right = 0
up = 0
down = 0

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

        def animateMoveDown(item):
            pygame.time.get_ticks(60)
            iterations = 60
            
            self.rect.y -= 1
            board[currentRow][colSplitCount]
            pass
            


    def removeItem():
        globs.SCREEN.blit(self.image, (self.x - 16, self.y - 11))
    
    def moveDownItem(self, picture_path, pos, itemSize):
        pass



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
    for r in range(ROW_COUNT):
        rowArray = []

        for c in range (COLUMN_COUNT):
            itemCount = itemCount + 1

            chosenItem = itemTypes[random.randint(0, itemLen-1)]
            itemPosition = [(c*itemSize + innerSpacing*c + outerLeftMargin), (r*itemSize + innerSpacing*r + outerTopMargin)]
            
            rowArray.append(chosenItem)

            itemSprite = Item(chosenItem, itemPosition, itemSize)
            itemGroup.add(itemSprite)
            #maybe add it after calculations
        
        board[r] = rowArray

    #INCLUDE THIS in the function somehow


def deleteItems(columnDict, rowDict):
    print("rows here")
    print(rowDict)

    currentRow = ROW_COUNT-1

    while currentRow >= 0:
        if currentRow in rowDict:
            print("it is in")
            print(currentRow)

            for colCount in rowDict[currentRow][1]:

                if type(colCount) is list:
                    
                    for colSplitCount in colCount:
                        i = colSplitCount-1
                        if colSplitCount != 0:
                            # There are multiple matches in an array

                            # The one below is being replaced with the one above
                            board[currentRow][colSplitCount] = board[i][colSplitCount]


                            # animateRemove(board[currentRow][colSplitCount])
                            # animateMoveDown(board[currentRow][colSplitCount])
                            # HERE!!!
                            
                        else:
                            chosenItem = itemTypes[random.randint(0, itemLen-1)]
                            print(board[colSplitCount])
                            board[currentRow][colSplitCount] = chosenItem


                # which columns are they?
                # they are the colCount

                #SET the row number to a variable - it is the currentRow
                else:
                    i = currentRow -1
                    if currentRow != 0:
                        print(board)
                        # time.sleep(2)
                        board[currentRow][colCount] = board[i][colCount]
                        print(board[i][colCount])
                        print("kjnsdzjkfjkzdfjkfdjkdfs")
                        print("THE ONES U NEED TO REPLACE")
                        print(' ')
                    else:
                        chosenItem = itemTypes[random.randint(0, itemLen-1)]
                        print(chosenItem)
                        print("kjdsjkfdskjl")
                        print(currentRow)
                        print(colCount)
                        print(board[currentRow][colCount])
                        board[currentRow][colCount] = chosenItem

            
                        
                        # need to spawn in new ones



                # board[]
                # print(" ")
                # print(colCount)

            # get the [1] part of the dictionary - for each one, get each number
            # then for each number go up every row and move the item down that is directly above it
            # spawn in new ones for the very top - pick random ones - you should make a function of spawning new ones***



        currentRow-=1

    print(board)
    # pygame.time.wait(5000)
    # plt.pause(2)

    # makeBoard(board)
    print("slept")



        #MOVE all of the items down 1
        #replace the top part with different colours
        #do like an animation thing

        #get the column number
        #then shift all of them down by 1 in the required column



    # print(board)
    # print("ZJLFJK")

    # print(columnDict)
    # print(rowDict)
    # print("hi")



def checkBoard(board, columnDict, rowDict):

    i = 0
    j = 1
        
    #See if there are multiple matches in a row
    for colKey in columnDict:
        colLen = len(columnDict[colKey][1])
        
        i = 0
        j = 1
        firstCol = []
        secondCol = []
        splitCol = False
        while j<colLen and splitCol != True:

            if columnDict[colKey][1][i] + 1 != columnDict[colKey][1][j]:
                colCount = 0
                firstCol = []
                secondCol = []

                while colCount < j:
                    firstCol.append(columnDict[colKey][1][colCount])
                    colCount += 1
                
                colCount = j
                    
                while colCount < len(columnDict[colKey][1]):
                    secondCol.append(columnDict[colKey][1][colCount])
                    colCount += 1

                columnDict[colKey][1] = []
                columnDict[colKey][1].append(firstCol)
                columnDict[colKey][1].append(secondCol) #####

                splitCol = True

            i+=1
            j+=1


    #See if there are multiple matches in a column
    for rowKey in rowDict:

        rowLen = len(rowDict[rowKey][1])
        
        i = 0
        j = 1
        firstRow = []
        secondRow = []
        splitRow = False
        while j<rowLen and splitRow != True:

            if rowDict[rowKey][1][i] + 1 != rowDict[rowKey][1][j]:
                rowCount = 0
                firstRow = []
                secondRow = []

                while rowCount < j:
                    firstRow.append(rowDict[rowKey][1][rowCount])
                    rowCount += 1

                rowCount = j
                    
                while rowCount < len(rowDict[rowKey][1]):
                    secondRow.append(rowDict[rowKey][1][rowCount])
                    rowCount += 1

                rowDict[rowKey][1] = []
                rowDict[rowKey][1].append(firstRow)
                rowDict[rowKey][1].append(secondRow) #####
                splitRow = True

            i+=1
            j+=1
    
    # deleteItems(columnDict, rowDict)


def itemCollect(board, itemTypes):
    # itemTypes: the different colors available

    # Check horizontal locations for 3-in-a-row items
    comboColumns = []
    comboRows = []
    rowMarker = 0
    columnMarker = 0

    rowComboDict = {}
    columnComboDict = {}

    # HORIZONTAL MATCHES
    for item in itemTypes:
        for r in range(ROW_COUNT):
            while columnMarker < COLUMN_COUNT-2:

                if board[r][columnMarker] == item and board[r][columnMarker+1] == item and board[r][columnMarker+2] == item:
                    comboColumns.extend([columnMarker, columnMarker+1, columnMarker+2])
                    columnMarker += 2

                    while columnMarker+1 < COLUMN_COUNT:
                        # Checking if it is longer than 3 in a row

                        if board[r][columnMarker+1] == item:
                            comboColumns.append(columnMarker + 1)
                            
                        else:
                            break

                        columnMarker += 1

                # GAP between them - see later
                else:
                    columnMarker += 1

            if len(comboColumns) > 0:
                rowComboDict[r] = [item, comboColumns]

            comboColumns = []
            columnMarker = 0
            

        # VERTICAL MATCHES
        for c in range(COLUMN_COUNT):
            while rowMarker < ROW_COUNT-2:

                if board[rowMarker][c] == item and board[rowMarker + 1][c] == item and board[rowMarker + 2][c] == item:
                    comboRows.extend([rowMarker, rowMarker+1, rowMarker+2])
                    rowMarker += 2

                    while rowMarker+1 < ROW_COUNT:
                        # Checking if it is longer than 3 in a column

                        if board[rowMarker + 1][c] == item:
                            comboRows.append(rowMarker + 1)
                            
                        else:
                            break

                        rowMarker += 1

                # GAP between them - see later
                else:
                    rowMarker += 1

            if len(comboRows) > 0:
                columnComboDict[c] = [item, comboRows]

            comboRows = []
            rowMarker = 0

    checkBoard(board, columnComboDict, rowComboDict)



itemCollect(board, itemTypes)







# Starting game
# board = create_board()
# draw_board(board)

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
