from operator import ne
from optparse import Values
import os, pygame, random, sys, math
from turtle import left, right
from unicodedata import name
import numpy as np
from os import system

# myFont = pygame.font.SysFont("monospace", 60)

ROW_COUNT = 8
COLUMN_COUNT = 8 

FPS = 60
clock = pygame.time.Clock()
pygame.init()

# Load all images


# BLUE = "blue"
# GREEN = 
# ORANGE = "orange"
# PURPLE = "purple"
# RED = "red"
# YELLOW = 


itemTypes = [
    "red",
    "yellow",
    "orange",
    "purple",
    "green",
    "blue"
]

SQUARESIZE = 10

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode((800, 800))

board = {}


# RED = (255, 0, 0)
# YELLOW = (255, 255, 0)
# ORANGE = (255, 165, 0)
# PURPLE = (128, 0, 128)
# GREEN = (0, 128, 2)
# BLUE = (0, 0, 255)

class Key(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, id):
        super(Key, self).__init__()
        self.i


# see where mouse is
# if the user is dragging,
# get their mouse position in x and y -> round them up/down to nearest square
# - dont work if in between squares
# smooth drag in between - movement

# if it is allowed, switch the positions. if not, don't
# - need to record a record of the different objects and grid to check with internal system



#later, make these images instead of just colors

rectangle_draging = False

itemLen = len(itemTypes)

itemArray = []


# def create_board():
#     board = board = np.zeros((ROW_COUNT, COLUMN_COUNT))
#     return board
    # Create a board


# def place_piece(board, row, col, piece):
#     board[row][col] = piece

rectangle = pygame.rect.Rect(176, 134, 17, 17)



image = ""

class Item(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos, itemSize):
        super().__init__()

        completeImgPath = os.path.join("images", (str(picture_path) + ".png"))
        #add checking here later

        self.image = pygame.image.load(completeImgPath)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]  #put x coord here
        self.rect.y = pos[1] # put y coord here
        self.width = itemSize
        self.height = itemSize
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        # the picture, and the rectangle around the picture

# need to load image
# define image before the class but they are different images

# class moveRight(pygame.sprite.Sprite):
#     def __init__(self, picture_path, pos, itemSize):





# HAVE a dictionary of all Values
# when player switches items, the values in the dict switch -> goes back into class




# newImg = Item(RED, )
itemGroup = pygame.sprite.Group()
# itemGroup.add(newImg)
itemSize = 80
innerSpacing = 5
outerTopMargin = 100
outerLeftMargin = 60

itemCount = 0

# IF there's 3 in a row, delete them and add new ones

#-----------------
#SAMPLE BOARDS

# VERTICAL 3 in a row
# board = {0: ['purple', 'yellow', 'yellow', 'blue', 'orange', 'green', 'green', 'blue'], 1: ['purple', 'blue', 'yellow', 'blue', 'yellow', 'purple', 'orange', 'orange'], 2: ['yellow', 'orange', 'blue', 'green', 'orange', 'orange', 'red', 'green'], 3: ['blue', 'orange', 'green', 'blue', 'blue', 'green', 'green', 'yellow'], 4: ['blue', 'green', 'blue', 'orange', 'red', 'purple', 'purple', 'yellow'], 5: ['orange', 'yellow', 'orange', 'yellow', 'blue', 'yellow', 'orange', 'yellow'], 6: ['yellow', 'red', 'purple', 'purple', 'yellow', 'red', 'red', 'orange'], 7: ['yellow', 'red', 'blue', 'yellow', 'purple', 'blue', 'orange', 'blue']}
#Only 1
# board = {0: ['red', 'red', 'orange', 'green', 'yellow', 'purple', 'purple', 'blue'], 1: ['red', 'yellow', 'red', 'yellow', 'yellow', 'orange', 'green', 'blue'], 2: ['orange', 'red', 'red', 'yellow', 'green', 'orange', 'orange', 'red'], 3: ['red', 'red', 'orange', 'green', 'red', 'orange', 'red', 'yellow'], 4: ['yellow', 'yellow', 'blue', 'green', 'red', 'green', 'green', 'orange'], 5: ['orange', 'red', 'orange', 'yellow', 'orange', 'blue', 'orange', 'orange'], 6: ['blue', 'blue', 'orange', 'orange', 'blue', 'green', 'green', 'yellow'], 7: ['purple', 'yellow', 'yellow', 'orange', 'blue', 'red', 'yellow', 'green']}

# VERTICAL 4 in a row
# board = {0: ['blue', 'yellow', 'purple', 'purple', 'green', 'red', 'green', 'purple'], 1: ['blue', 'red', 'green', 'green', 'blue', 'orange', 'orange', 'orange'], 2: ['green', 'blue', 'red', 'orange', 'green', 'green', 'red', 'red'], 3: ['green', 'purple', 'purple', 'orange', 'red', 'blue', 'red', 'yellow'], 4: ['orange', 'purple', 'orange', 'blue', 'red', 'yellow', 'blue', 'blue'], 5: ['green', 'orange', 'purple', 'blue', 'red', 'blue', 'yellow', 'green'], 6: ['green', 'green', 'purple', 'orange', 'red', 'purple', 'yellow', 'orange'], 7: ['orange', 'green', 'red', 'blue', 'orange', 'yellow', 'blue', 'blue']}

# HORIZONTAL 3 in a row
# board = {0: ['green', 'purple', 'purple', 'yellow', 'purple', 'red', 'purple', 'blue'], 1: ['yellow', 'blue', 'red', 'orange', 'blue', 'purple', 'green', 'green'], 2: ['yellow', 'red', 'yellow', 'orange', 'green', 'red', 'purple', 'green'], 3: ['red', 'blue', 'red', 'green', 'blue', 'blue', 'purple', 'blue'], 4: ['green', 'yellow', 'orange', 'orange', 'red', 'blue', 'green', 'yellow'], 5: ['green', 'blue', 'purple', 'green', 'green', 'green', 'blue', 'green'], 6: ['blue', 'blue', 'red', 'red', 'blue', 'blue', 'purple', 'green'], 7: ['purple', 'yellow', 'yellow', 'blue', 'red', 'yellow', 'yellow', 'blue']}

# HORIZONTAL 4 in a row
board = {0: ['purple', 'purple', 'green', 'yellow', 'green', 'purple', 'red', 'yellow'], 1: ['red', 'red', 'yellow', 'blue', 'purple', 'red', 'blue', 'orange'], 2: ['red', 'orange', 'green', 'purple', 'red', 'green', 'orange', 'blue'], 3: ['green', 'red', 'purple', 'green', 'red', 'red', 'red', 'red'], 4: ['blue', 'blue', 'red', 'green', 'purple', 'blue', 'purple', 'orange'], 5: ['purple', 'green', 'green', 'yellow', 'blue', 'purple', 'green', 'green'], 6: ['yellow', 'green', 'green', 'green', 'green', 'purple', 'orange', 'orange'], 7: ['red', 'green', 'red', 'orange', 'orange', 'red', 'purple', 'red']}

# MULTIPLES
# board = {0: ['green', 'green', 'purple', 'green', 'yellow', 'yellow', 'purple', 'red'], 1: ['green', 'yellow', 'green', 'green', 'yellow', 'blue', 'blue', 'orange'], 2: ['green', 'red', 'yellow', 'purple', 'green', 'orange', 'yellow', 'blue'], 3: ['blue', 'blue', 'blue', 'purple', 'green', 'green', 'blue', 'green'], 4: ['purple', 'purple', 'red', 'yellow', 'yellow', 'green', 'green', 'blue'], 5: ['purple', 'blue', 'yellow', 'red', 'purple', 'blue', 'red', 'yellow'], 6: ['red', 'purple', 'yellow', 'blue', 'blue', 'green', 'yellow', 'purple'], 7: ['orange', 'red', 'yellow', 'green', 'blue', 'blue', 'yellow', 'red']}



#END SAMPLE BOARDS
#-----------------


if len(board) > 0:
    testDict = True
    dictionaryLen = len(board)
else:
    testDict = False


if testDict == True:
            r = 0
            for r, columnArray in board.items():
                
                c = 0
                for chosenItem in columnArray:

                    itemPosition = [(c*itemSize + innerSpacing*c + outerLeftMargin), (r*itemSize + innerSpacing*r + outerTopMargin)]
                    itemSprite = Item(chosenItem, itemPosition, itemSize)

                    itemGroup.add(itemSprite)
                    c+=1

                r += 1

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





# for item in board:

#     if board [r]

#HERE

def itemCollect(board, itemTypes):
    # itemTypes: the different colours available

    # Check horizontal locations for 3-in-a-row items
    comboColumns = []
    rowMarker = 0
    columnMarker = 0

    for item in itemTypes:
        # print(itemTypes)
        
        for r in range(ROW_COUNT-2):
            while columnMarker < COLUMN_COUNT-2:
                if columnMarker == COLUMN_COUNT:
                    comboColumns = []
                    columnMarker = 0
                    break

            
            print(str(board[r][columnMarker + 1]) + " " + str(board[r+1][columnMarker]) + " " + str(board[r+2][columnMarker]))
            print("ggg")


        


            
            # for each column (c)

            # REPLACE THIS
            #which column
            
            # for r in range(ROW_COUNT):
                # print(" ")
                # print(board[c][r])

            # print(c)
            # print("zdddd")
            
            while rowMarker < ROW_COUNT-2:

                # print(board[rowMarker])

                # BOARD is arranged - rows first (rowMarker), then columns ()

                # print(board[r][c] + " " + board[r][c+1] + " " + board[r][c+2] + " ")
                # See if there are three in a row
                if rowMarker == ROW_COUNT:
                    comboColumns = []
                    rowMarker = 0
                    break
                

                print(str(board[rowMarker][c]) + " " + str(board[rowMarker][c+1]) + " " + str(board[rowMarker][c+2]))
                print("  ")

                print(str(rowMarker) + " " + str(c))


                if board[rowMarker][c] == item and board[rowMarker][c+1] == item and board[rowMarker][c+2] == item:
                    comboColumns.extend([c, c+1, c+2])
                    
                    # print("")
                    # print(c)
                    # print(board[rowMarker])
                    #board[colMarker] is the array in which the 3 in a row occurs

                    # print("HERE")
                    rowMarker += 2
                    
                    #Check if next tile is also the item

                    nextItemChecker = rowMarker + 1
                    print(comboColumns)
                    

                    while nextItemChecker <= ROW_COUNT:
                        print(" ")
                        print("HI")
                        print(item)
                        print(board[rowMarker][nextItemChecker])

                        if board[rowMarker][nextItemChecker] == item:
                            comboColumns.append(rowMarker)
                            nextItemChecker += 1

                        else:
                            if rowMarker < ROW_COUNT:
                                rowMarker += 1
                            break

                    #HERE
                    # replaceItems(r, rowComboColumns)

                
                    # while rightOfCombo > 0:
                    #     if board[r][rightOfCombo] == item:
                    #         itemCombo.append()

                    #     rightofcombo - eg. there are 4 to the left
                    #     so board[r][rightofcombo-1] to get the one that is 3rd
                    #HERE


                    # see if right next to it is the same or not
                    # if it is the same, see if next one is the same etc. 
                    # do this for left and right
                    # - check if the columns have ended or not


                    # - right, left
                    # have limits - eg. r 

                    
                    # leftDistance = COLUMN_COUNT - c
                    # print(rowComboColumns)
                    # print("left: " + str(c)  + ", right: " + str(COLUMN_COUNT -(c+3)))

                    # if c != 0:

                    #     print('')
                    # chosenItem = itemTypes[random.randint(0, itemLen-1)]
                    # itemPosition = [(c*itemSize + innerSpacing*c + outerLeftMargin), (r*itemSize + innerSpacing*r + outerTopMargin)]
                    # board.replace(board[r][c], chosenItem)

                    # chosenItem = itemTypes[random.randint(0, itemLen-1)]
                    # board.replace(board[r][c+1], chosenItem)

                    # chosenItem = itemTypes[random.randint(0, itemLen-1)]
                    # board.replace(board[r][c+2], chosenItem)

                    print("horizontal " + str(item) + " - " + str(comboColumns))
                    # return True

                rowMarker +=1
                print(rowMarker)
                print(" HHHH")
    
    # Check vertical locations for potential 3-in-a-row items
    for item in itemTypes:
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-2):
                if board[r][c] == item and board[r+1][c] == item and board[r+2][c] == item:
                    # board.replace(board[r][c], )
                    print("vertical " + str(item))
                    # return True
    
    return
#HERE

# def newItems(board, itemTypes):

   
# # def rearrangeBoard(board, itemTx


itemCollect(board, itemTypes)
# if itemCollect(board, itemTypes) == True:
#     print("HIII")

# print(board[3][5]) FIRST VAL (3): THE KEY (THE ROW), SECOND VAL (5): THE ITEM LOC. NO (COLUMNS ALONG)
# print(board[1][2])
# print(board[0][0])
# print(board[7][7])
# print("Hey")






# Starting game
# board = create_board()
# draw_board(board)
game_over = False
turn = 0


print(board)


while not game_over:
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
    clock.tick(FPS)
    itemGroup.draw(screen)

pygame.quit()
