
import random, math
# from unicodedata import name
# import numpy as np
# from os import system
# import time
import globs

def shiftDown(col):
    col.reverse()
    itemNo = 0
    modifiedItems = []
    
    for item in col:
        
        if item == "BLANK":
            unchangedCol = col[:itemNo]
            unchangedLen = len(unchangedCol)

            while unchangedLen < globs.COLUMN_COUNT:
                unchangedCol.append("BLANK")
                unchangedLen += 1

            col.pop(itemNo)
            newItem = globs.itemTypes[random.randint(0, globs.itemLen-1)]
            col.append(newItem)

            col.reverse()
            unchangedCol.reverse()

            reversedItemNo = globs.COLUMN_COUNT-1 - itemNo
            
            # Get center things
            i = 0
            while i<= reversedItemNo:
                if col[i] != "BLANK":
                    modifiedItems.append(i)
                i += 1
            
            return modifiedItems, unchangedCol, col

        itemNo+=1


def itemCollectVertical(board, itemTypes):
    # Check horizontal locations for 3-in-a-row items
    comboCols1 = []
    rowMarker = 0
    colComboDict = {}

    # HORIZONTAL MATCHES
    for item in itemTypes:
        for c in range(globs.COLUMN_COUNT):
            while rowMarker < globs.ROW_COUNT-2:
                # if board[c][row]

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
                colComboDict[colKey].append(secondCol)
                splitCol = True

            i+=1
            j+=1

    return(colComboDict)
    

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
                else:
                    colMarker += 1

            if len(comboRows) > 0:
                rowComboDict[r] = [item, comboRows]

            comboRows = []
            colMarker = 0

    # See if there are multiple matches in a row
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