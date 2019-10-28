from GameBoard  import Board
from Computer_AI import ComputerAI
from Player_AI   import PlayerAI
from Displayer import Displayer
from random import randint
import time

#Number of Initial values to be generated randomly
defaultInitialTiles = 2
#The value 2 is generated with probability 90%
defaultProbability = 0.9

#The possible actions
actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

#Computer:1 and Player:0
(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

#Time limit before losing
timeLimit = 0.2
allowance = 0.2


class GameManager:
    def __init__(self, size = 4):
        self.grid = Board(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles  = defaultInitialTiles
        self.computerAI = None
        self.playerAI   = None
        self.displayer  = None
        self.over       = False

    def setComputerAI(self, computerAI):
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI

    def setDisplayer(self, displayer):
        self.displayer = displayer

    #time since a Player_AI has started playing
    def updateAlarm(self, currTime):
        if currTime - self.prevTime > timeLimit + allowance:
            self.over = True
        else:
            while time.clock() - self.prevTime < timeLimit + allowance:
                pass

            self.prevTime = time.clock()

   #start the game of 2048
    def start(self,str):
        startTime=time.clock()
        print("Start the game with alpha beta pruning:",str=="Pruning")
        #generate 2 tiles randomly of value 2 or 4
        for i in range(self.initTiles):
            self.insertRandomTile()
          #display the initial board
        self.displayer.display(self.grid)
        # Player AI Goes First
        turn = PLAYER_TURN
        maxTile = 0
        #record the game start time
        self.prevTime = time.clock()
        #while time limit is not exceeded and sliding is still posiible
        while not self.isGameOver() and not self.over:
            # Copy to Ensure AI Cannot Change the Real Grid to Cheat
            gridCopy = self.grid.clone()
            move = None
            if turn == PLAYER_TURN:
                print("Player's Turn:")
                #get next move which leads to maximum utility
                move = self.playerAI.getMove(gridCopy,str)
                print(actionDic[move])
                # Validate Move
                if move != None and move >= 0 and move < 4:
                    if self.grid.canSlide([move]):
                        #slide the grid
                        self.grid.slide(move)
                        #Get maximum value on board
                        maxTile = self.grid.getMaxValueOnBoard()
                    else:
                        print("Invalid PlayerAI Move")
                        self.over = True
                else:
                    print("Invalid PlayerAI Move - 1")
                    self.over = True
            else:
                #Computers turn generate a random tile on board
                print("Computer's turn:")
                #get next position
                position = self.computerAI.getRandomPosition(gridCopy)
                # Validate Move
                #check if position is empty
                if position and self.grid.canInsert(position):
                    #insert 2 or 4 in that position
                    self.grid.setCellValue(position, self.getNewTileValue())
                else:
                    print("Invalid Computer AI Move")
                    self.over = True
             #If time limit not exceeded dispaly grid
            if not self.over:
                self.displayer.display(self.grid)
            # Exceeding the Time Allotted for Any Turn Terminates the Game
            self.updateAlarm(time.clock())
            #next player turn in next itertion
            turn = 1 - turn
         #if game has ended print max tile
        stopTime=time.clock()
        print("Time Taken ",stopTime-startTime)
        print(maxTile)

    #Retirn true if sliding is possible
    def isGameOver(self):
        return not self.grid.canSlide()

    #With probability of 90% generate next tile value as 2 or 4
    def getNewTileValue(self):
        if randint(0,99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1]

    #insert generated value in a random cell
    def insertRandomTile(self):
        tileValue = self.getNewTileValue()
        cells = self.grid.getEmptycells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)

def main():
    gameManager = GameManager()
    playerAI  	= PlayerAI()
    computerAI  = ComputerAI()
    displayer 	= Displayer()

    gameManager.setDisplayer(displayer)
    gameManager.setPlayerAI(playerAI)
    gameManager.setComputerAI(computerAI)
    #For game with alpha-beta pruning set it as Pruning else set Not pruning
    gameManager.start("Without Pruning")

if __name__ == '__main__':
    main()
