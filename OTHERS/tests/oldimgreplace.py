from operator import ne
from optparse import Values
import os, pygame, random, sys, math
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


def create_board():
    board = board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board
    # Create a board


def place_piece(board, row, col, piece):
    board[row][col] = piece

rectangle = pygame.rect.Rect(176, 134, 17, 17)

board = []

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
    
    board.append(rowArray)


# IF there's 3 in a row, delete them and add new ones


# for item in board:

#     if board [r]

def itemCollect(board, itemTypes):
    # Check horizontal locations for 3-in-a-row items
    for item in itemTypes:
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                # print(board[r][c] + " " + board[r][c+1] + " " + board[r][c+2] + " " + board[r][c+3])
                # See if there are three in a row
                if board[r][c] == item and board[r][c+1] == item and board[r][c+2] == item and board[r][c+3] == item:
                    
                    board.remove(board[r][c+2])
                    board.remove(board[r][c+3])

                    chosenItem = itemTypes[random.randint(0, itemLen-1)]
                    itemPosition = [(c*itemSize + innerSpacing*c + outerLeftMargin), (r*itemSize + innerSpacing*r + outerTopMargin)]
                    board.replace(board[r][c], chosenItem)

                    chosenItem = itemTypes[random.randint(0, itemLen-1)]
                    board.replace(board[r][c+1], chosenItem)

                    chosenItem = itemTypes[random.randint(0, itemLen-1)]
                    board.replace(board[r][c+2], chosenItem)
                    #need to replace later


                    print("vertical")
                    return True
    
    # Check vertical locations for potential 3-in-a-row items
    for item in itemTypes:
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == item and board[r+1][c] == item and board[r+2][c] == item and board[r+3][c] == item:
                    print("vertical")
                    return True
    
    return False

def newItems(board, itemTypes):

   
# def rearrangeBoard(board, itemTx



if itemCollect(board, itemTypes) == True:
    print("HIII")
    # rearrangeBoard(board, itemTypes)
# print(hi)



# search for it in the thing under the name
# only join it in the function
# - ONLY in the class





# def draw_board(board):
#     for c in range(COLUMN_COUNT):
#         for r in range(ROW_COUNT):
            # itemGroup = pygame.sprite.Group()
            # chosenItem = itemTypes[random.randint(0, itemLen-1)]
            # itemGroup.add(chosenItem)
            # print(itemGroup)
            # print((c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE), chosenItem.convert_alpha())
            # print('HELLO')
            # itemImage = Item((c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE), chosenItem.convert_alpha())
            # print(itemImage)
            # print("HI")

            # pygame.draw.rect(screen, chosenItem, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            # rectangle = pygame.rect.Rect(c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)
            # print(itemImage)
            # itemDictionary[chosenItem] = [c, rectangle]
            # print(chosenItem)
            # print(rectangle)
            # print("hi")

# player1 = Item((100, 300), pygame.image.load("an_image.png").convert_alpha())



# def print_board(board):
#     pass


# Starting game
board = create_board()
# draw_board(board)
game_over = False
turn = 0



#use setup like in short test but put it into here




print("zzz")

while not game_over:
    # event.button 1 -> left click
    # event.button 2 -> right click
    #event.button 3 -> middle click

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print("hi")
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
