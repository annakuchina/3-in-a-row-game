from operator import ne
from optparse import Values
import os, pygame, random, sys, math
from unicodedata import name
import numpy as np
from os import system
import time
import globs
# from newgame import ROW_COUNT, COLUMN_COUNT, itemTypes


def deleteItems(columnDict, rowDict, board):

    currentRow = globs.ROW_COUNT-1

    while currentRow >= 0:
        if currentRow in rowDict:

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


            # get the [1] part of the dictionary - for each one, get each number
            # then for each number go up every row and move the item down that is directly above it
            # spawn in new ones for the very top - pick random ones - you should make a function of spawning new ones***



        currentRow-=1

    print(board)



        #MOVE all of the items down 1
        #replace the top part with different colours
        #do like an animation thing

        #get the column number
        #then shift all of them down by 1 in the required column




# def checkBoard(board, columnDict, rowDict):
    
    
#     # print(columnDict, rowDict)
    
#     # deleteItems(columnDict, rowDict, board)




def itemCollectVertical(board, itemTypes):
    # itemTypes: the different colors available

    # Check horizontal locations for 3-in-a-row items
    comboCols1 = []
    rowMarker = 0
    colComboDict = {}
    

    # HORIZONTAL MATCHES
    for item in itemTypes:
        for c in range(globs.COLUMN_COUNT):
            while rowMarker < globs.ROW_COUNT-2:

                if board[c][rowMarker] == item and board[c][rowMarker+1] == item and board[c][rowMarker+2] == item:
                    comboCols1.extend([rowMarker, rowMarker+1, rowMarker+2])
                    rowMarker += 2

                    while rowMarker+1 < globs.ROW_COUNT:
                        # Checking if it is longer than 3 in a row

                        if board[c][rowMarker+1] == item:
                            comboCols1.append(rowMarker + 1)
                            
                        else:
                            break

                        rowMarker += 1

                # GAP between them - see later
                else:
                    rowMarker += 1

            if len(comboCols1) > 0:
                colComboDict[c] = [item, comboCols1]

            comboCols1 = []
            rowMarker = 0
            
    for colKey in colComboDict:
        colLen = len(colComboDict[colKey][1])
        
        i = 0
        j = 1
        firstCol = []
        secondCol = []
        splitCol = False
        while j<colLen and splitCol != True:

            if colComboDict[colKey][1][i] + 1 != colComboDict[colKey][1][j]:
                colCount = 0
                firstCol = []
                secondCol = []

                while colCount < j:
                    firstCol.append(colComboDict[colKey][1][colCount])
                    
                    colCount += 1

                colCount = j
                    
                while colCount < len(colComboDict[colKey][1]):
                    secondCol.append(colComboDict[colKey][1][colCount])
                    colCount += 1

                colComboDict[colKey].pop()
                colComboDict[colKey].append(firstCol)
                colComboDict[colKey].append(secondCol) #####
                splitCol = True

            i+=1
            j+=1

    # this one is rowComboDict
        

    return(colComboDict)
    # checkBoard(board, columnComboDict, rowComboDict)



def itemCollectHorizontal(board, itemTypes):
    colMarker = 0
    comboRows = []
    rowComboDict = {}

    # VERTICAL MATCHES
    for item in itemTypes:
        for r in range(globs.ROW_COUNT):
            while colMarker < globs.COLUMN_COUNT-2:

                if board[colMarker][r] == item and board[colMarker + 1][r] == item and board[colMarker + 2][r] == item:
                    comboRows.extend([colMarker, colMarker+1, colMarker+2])
                    colMarker += 2

                    while colMarker+1 < globs.COLUMN_COUNT:
                        # Checking if it is longer than 3 in a column

                        if board[colMarker + 1][r] == item:
                            comboRows.append(colMarker + 1)
                            
                        else:
                            break

                        colMarker += 1

                # GAP between them - see later
                else:
                    colMarker += 1

            if len(comboRows) > 0:
                rowComboDict[r] = [item, comboRows]

            comboRows = []
            colMarker = 0

     #See if there are multiple matches in a row
    for rowKey in rowComboDict:
        rowLen = len(rowComboDict[rowKey][1])
        
        i = 0
        j = 1
        firstRow = []
        secondRow = []
        splitRow = False
        while j<rowLen and splitRow != True:

            if rowComboDict[rowKey][1][i] + 1 != rowComboDict[rowKey][1][j]:
                rowCount = 0
                firstRow = []
                secondRow = []

                while rowCount < j:
                    firstRow.append(rowComboDict[rowKey][1][rowCount])
                    rowCount += 1
                
                rowCount = j
                    
                while rowCount < len(rowComboDict[rowKey][1]):
                    secondRow.append(rowComboDict[rowKey][1][rowCount])
                    rowCount += 1

                rowComboDict[rowKey].pop()
                rowComboDict[rowKey].append(firstRow)
                rowComboDict[rowKey].append(secondRow)

                splitRow = True

            i+=1
            j+=1

    return(rowComboDict)
    # this one is columnComboDict

