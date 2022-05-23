import python

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