from random import randint
import numpy as np
import time

#x and y coordinate of up down left and right vectors for addition
directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

class PlayerAI():
    depth = 0
    time = 0

    #get Player move either with or without alpha beta pruning
    def getMove(self, grid, str):
        self.depth = 0
        self.time = time.clock()
        #If "Pruning" initiate alpha beta pruning
        if str == "Pruning":
            (maxChild, maxUtility) = self.maximize(grid, -float('inf'), float('inf'))
        else:
            (maxChild, maxUtility) = self.withoutpruning(grid, -float('inf'), float('inf'))
        #direction vector of chosen slide direction
        move = maxChild[1]
        return move

    #The player has gone to a certain depth so terminate
    def timeup(self, depth):
        diff = time.clock() - self.time
        if diff >= 0.1 / depth:
            return True
        else:
            return False

    #return the tuple (board, each possible move)
    def legalmoves(self, board):
        children = []
        if board.canSlide():
            for move in board.getAvailableMoves():
                boardcopy = board.clone()
                boardcopy.slide(move)
                children.append((boardcopy, move))
        return children

    #populate each empty cell with 2
    def populate_emptycell(self, grid):
        children = []
        for cell in grid.getEmptycells():
            child = grid.clone()
            child.setCellValue(cell, 2)
            children.append(child)
        return children

    #caculating beta value
    def minimize(self, grid, alpha, beta):
        #if player has taken much time or no more empty cells then we have reached the terminal state so calculate utility
        if self.timeup(self.depth + 1) or not grid.getEmptycells():
            return (None, self.evaluate(grid))
        #minUtility =beta=-inf
        (minChild, minUtility) = (None, float('inf'))
        #calculate next depth(Computer turn) take minimum utility child among all childs
        self.depth += 1
        #for each child in next depth populate one cell randomly with 2
        for child in self.populate_emptycell(grid):
            #calculate utility
            (_, utility) = self.maximize(child, alpha, beta)
            #if utility is less than minUtility
            if utility < minUtility:
                (minChild, minUtility) = (child, utility)
                #if alpha becomes greater than equal to beta return beta(minUtility)
            if minUtility <= alpha:
                return (minChild, minUtility)
            #if beta is less than utility then assign  beta as minUtility
            if minUtility < beta:
                beta = minUtility
        return (minChild, minUtility)

        # caculating beta value without pruning
    def minimize_withoutpruning(self, grid, alpha, beta):
        # if player has taken much time or no more empty cells then we have reached the terminal state so calculate utility
        if self.timeup(self.depth + 1) or not grid.getEmptycells():
            return (None, self.evaluate(grid))
        # minUtility =beta=-inf
        (minChild, minUtility) = (None, float('inf'))
        # calculate next depth(Computer turn) take minimum utility child among all childs
        self.depth += 1
        # for each child in next depth populate one cell randomly with 2
        for child in self.populate_emptycell(grid):
            # calculate utility
            (_, utility) = self.maximize(child, alpha, beta)
            # if utility is less than minUtility
            if utility < minUtility:
                (minChild, minUtility) = (child, utility)
            # if beta is less than utility then assign  beta as minUtility
            if minUtility < beta:
                beta = minUtility
        return (minChild, minUtility)


    #minimax with alpha beta pruning :select first legal move with alpha>=beta
    def maximize(self, grid, alpha, beta):
        #while sliding is not possible
        if not grid.getAvailableMoves():
            #calculate evaluation function
            return (None, self.evaluate(grid))
        #assign Maxutility as -inf
        (maxChild, maxUtility) = (None, -float('inf'))
        #next depth level (Computer turn)
        self.depth += 1
        #for each legal move on the board calculate each possible child at next depth(computer turn)
        for child in self.legalmoves(grid):

            #calculate utility for each legal move with alpha beta as -inf and inf
            (_, utility) = self.minimize(child[0], alpha, beta)
            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)
                #alpha>=beta then prune
            if maxUtility >= beta:
                return (maxChild, maxUtility)
            #assign alpha as maxUtility
            if maxUtility > alpha:
                alpha = maxUtility
        return (maxChild, maxUtility)

    #minimax without alpha beta pruning
    def withoutpruning(self, grid,alpha,beta):
        # while sliding is not possible
        if not grid.getAvailableMoves():
            # calculate evaluation function
            return (None, self.evaluate(grid))
        # assign Maxutility as -inf
        (maxChild, maxUtility) = (None, -float('inf'))
        # next depth level (Computer turn)
        self.depth += 1
        # for each legal move on the board calculate each possible child at next depth(computer turn)
        for child in self.legalmoves(grid):
            # calculate utility for each legal move with alpha beta as -inf and inf
            (_, utility) = self.minimize(child[0], alpha, beta)
            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)
            # assign alpha as maxUtility
            if maxUtility > alpha:
                alpha = maxUtility
        return (maxChild, maxUtility)


    #choose 2 with probability 90% and 4 with probability 10%
    def getNewTileValue(self):
        if randint(0, 99) < 90:
            return 2
        else:
            return 4

   #if cell value !=0: True
    def cellOccupied(self, grid, pos):
        return not not grid.getCellValue(pos)

    #calculate utility function
    def evaluate(self, grid, prt=False):
        emptycells = len(grid.getEmptycells())
        empty = emptycells if emptycells else 1
        #weights of each heuristic
        smoothWeight = 0.5
        monotonicityWeight = 3.0 / empty
        emptinessWeight = 2.7 / empty
        maxTileWeight = 4.0
        #weighted heuristics
        smooth = self.smoothness(grid) * smoothWeight
        monoton = self.monotonicity(grid) * monotonicityWeight
        emptiness = np.log(empty) * emptinessWeight
        maxval = self.max4tile(grid) * maxTileWeight
        #total utility function is summation of heuristic
        total = smooth + monoton + emptiness + maxval
        return total

    # from (0,0) find the smoothness in the right and down direction smoothness=|value-nextvalue|
    def smoothness(self, grid):
        smoothness = 0
        for i in range(4):
            for j in range(4):
                if not grid.canInsert((i, j)):
                    value = np.log(grid.map[i][j]) / np.log(2)
                    for vector in [RIGHT_VEC, DOWN_VEC]:
                        targetCell = self.findfarthest(grid, (i, j), vector)
                        if self.cellOccupied(grid, targetCell):
                            target = grid.getCellValue(targetCell)
                            targetValue = np.log(target) / np.log(2)
                            smoothness -= abs(value - targetValue)
        return smoothness

    #find the next cell with value in the director of direction vector
    def findfarthest(self, grid, cell, vector):
        while True:
            prev = cell
            cell = (prev[0] + vector[0], prev[1] + vector[1])
            if not grid.checkingBoundary(cell) and grid.canInsert(cell):
                continue
            else:
                return cell

    def max4tile(self, grid):
        arr = np.array(grid.map).reshape(16)
        top = np.sort(arr)[-4::]
        val = np.sum(top * np.array([1, 2, 4, 8]))
        return np.log(val)

    #check monotonicity in down and right direction
    def monotonicity(self, grid):
        totals = [0, 0, 0, 0]
        # up/down
        for i in range(4):
            current = 0
            nxt = current + 1
            while nxt < 4:
                while nxt < 4 and grid.canInsert((i, nxt)):
                    nxt += 1
                if nxt >= 4:
                    nxt -= 1
                currentValue = np.log(grid.getCellValue((i, current))) / np.log(2) if not grid.canInsert(
                    (i, current)) else 0
                nextValue = np.log(grid.getCellValue((i, nxt))) / np.log(2) if not grid.canInsert((i, nxt)) else 0
                if currentValue > nextValue:
                    totals[0] += nextValue - currentValue
                elif nextValue > currentValue:
                    totals[1] += currentValue - nextValue
                current = nxt
                nxt += 1
        # left/right
        for j in range(4):
            current = 0
            nxt = current + 1
            while nxt < 4:
                while nxt < 4 and grid.canInsert((nxt, j)):
                    nxt += 1
                if nxt >= 4:
                    nxt -= 1
                currentValue = np.log(grid.getCellValue((current, j))) / np.log(2) if not grid.canInsert(
                    (current, j)) else 0
                nextValue = np.log(grid.getCellValue((nxt, j))) / np.log(2) if not grid.canInsert((nxt, j)) else 0
                if currentValue > nextValue:
                    totals[2] += nextValue - currentValue
                elif nextValue > currentValue:
                    totals[3] += currentValue - nextValue
                current = nxt
                nxt += 1
        return max(totals[0], totals[1]) + max(totals[2], totals[3])


