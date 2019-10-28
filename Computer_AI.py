from random import randint

#Computer AI chooses random empty cell to insert 2 or 4
class ComputerAI():
    def getRandomPosition(self, grid):
        cells = grid.getEmptycells()
        #choose a random cell in list of empty cell
        return cells[randint(0, len(cells) - 1)] if cells else None
