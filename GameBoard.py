from copy import deepcopy

#x and y coordinate of up down left and right vectors for addition
directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
#directions in which the game can be swipped
direction = [UP, DOWN, LEFT, RIGHT] = range(4)

class Board:
    #generate a 4*4 board with values
    #0       0       0       0
    #0       0       0       0
    #0       0       0       0
    #0       0       0       0
    def __init__(self, size = 4):
        self.size = size
        self.map = [[0] * self.size for i in range(self.size)]

    # Make a Deep Copy of the current board
    def clone(self):
        boardcopy = Board()
        boardcopy.map = deepcopy(self.map)
        boardcopy.size = self.size
        return boardcopy

    # Insert a Value in an Empty Cell
    def setCellValue(self, pos, value):
        self.map[pos[0]][pos[1]] = value

    # Return All the Empty Cells
    def getEmptycells(self):
        cells = []
        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y] == 0:
                    cells.append((x,y))
        return cells

    # Return the Maximum Value on the Board
    def getMaxValueOnBoard(self):
        maxTile = 0
        for x in range(self.size):
            for y in range(self.size):
                maxTile = max(maxTile, self.map[x][y])
        return maxTile

    # Check if a value can be inserted in a position: True/False
    def canInsert(self, pos):
        return self.getCellValue(pos) == 0

    #Sliding in the grid
    def slide(self, dir):
        dir = int(dir)
        #to move UP set moveDownorUp to False
        if dir == UP:
            return self.moveDownorUp(False)
        # to move DOWN set moveDownorUp to True
        if dir == DOWN:
            return self.moveDownorUp(True)
        #to move left set moveRightorLeft to False
        if dir == LEFT:
            return self.moveRightorLeft(False)
        # to move right set moveRightorLeft to True
        if dir == RIGHT:
            return self.moveRightorLeft(True)

    # Slide Up or Down
    def moveDownorUp(self, down):
        #calculate the range of movement
        r = range(self.size -1, -1, -1) if down else range(self.size)
        moved = False
        #go column by column merging cell values
        for j in range(self.size):
            cells = []
            for i in r:
                cell = self.map[i][j]
                #if cell has value
                if cell != 0:
                    cells.append(cell)
             #merge all cells which have value
            self.merge(cells)
            #pop the final caculated value after merging
            for i in r:
                value = cells.pop(0) if cells else 0
                #if the final calculated value is not the same as the value of the cell then there is movement
                if self.map[i][j] != value:
                    moved = True
                # assign the final calculated value to first or last row in the respective column j
                self.map[i][j] = value
        return moved

    # Slide left or right
    def moveRightorLeft(self, right):
        r = range(self.size - 1, -1, -1) if right else range(self.size)
        moved = False
        #go row by row merging cell values
        for i in range(self.size):
            cells = []
            for j in r:
                cell = self.map[i][j]
                if cell != 0:
                    cells.append(cell)
            self.merge(cells)
            for j in r:
                value = cells.pop(0) if cells else 0
                if self.map[i][j] != value:
                    moved = True
                # assign the final calculated value to first or last column in the respective row i
                self.map[i][j] = value
        return moved

    # Merge Tiles
    def merge(self, cells):
        #if zero or one cell has a value !=0
        if len(cells) <= 1:
            return cells
        i = 0
        while i < len(cells) - 1:
            #if the adjacent cells have same value then increase the value 2 times and store it at i position
            if cells[i] == cells[i+1]:
                cells[i] *= 2
                #delete the same adjacent value
                del cells[i+1]
            i += 1

    #Check if sliding into adjacent cell is possible from current cell
    def canSlide(self, dirs = direction):
        #Intial moves UP DOWN LEFT RIGHT
        checkingMoves = set(dirs)
        for x in range(self.size):
            for y in range(self.size):
                # If Current Cell has value!=0
                if self.map[x][y]:
                    #Looking into the possible adjacent cells
                    for i in checkingMoves:
                        move = directionVectors[i]
                        #get adjacent cell value
                        adjCellValue = self.getCellValue((x + move[0], y + move[1]))
                        # If Value is the Same or Adjacent Cell is same as current cell or if the adjacent cell is value=0 then return True
                        if adjCellValue == self.map[x][y] or adjCellValue == 0:
                            return True
                # Else if Current Cell has value=0 then return true
                elif self.map[x][y] == 0:
                    return True
        #no move possible next
        return False

    # Return All Directions in which sliding is possible
    def getAvailableMoves(self, dirs = direction):
        availableMoves = []
        for x in dirs:
            boardcopy = self.clone()
            if boardcopy.slide(x):
                availableMoves.append(x)
        return availableMoves

    #check if position (x,y) crosses 4*4 boundary
    def checkingBoundary(self, pos):
        return pos[0] < 0 or pos[0] >= self.size or pos[1] < 0 or pos[1] >= self.size

    #Get the value in the cell at a given position if that position is valid
    def getCellValue(self, pos):
        if not self.checkingBoundary(pos):
            return self.map[pos[0]][pos[1]]
        else:
            return None