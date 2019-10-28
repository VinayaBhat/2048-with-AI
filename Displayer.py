#!/usr/bin/env python
#coding:utf-8
import platform

#color map for values
colorMap = {0     : 97,
                        2     : 101,
                        4     : 100,
                        8     : 44,
                        16    : 101,
                        32    : 46,
                        64    : 106,
                        128   : 44,
                        256   : 104,
                        512   : 42,
                        1024  : 102,
                        2048  : 43,
                        4096  : 103,
                        8192  : 45,
                        16384 : 105,
                        32768 : 41,
                        65536 : 101,
                        }

#Display color and number scheme
cTemp = '\x1b[%dm%7s\x1b[0m '

#check the platform the code is running on: Windows/Unix
class Displayer():
        def __init__(self):
                if 'Windows' == platform.system():
                        self.display = self.windowsDisplay
                else:
                        self.display = self.unixDisplay

        def display(self, grid):
                pass

        #Windows display code
        def windowsDisplay(self, grid):
            for i in range(grid.size):
                for j in range(grid.size):
                    print("%6d  " % grid.map[i][j], end="")
                print("")
            print("")

        #Unix display code
        def unixDisplay(self, grid):
                for i in range(3 * grid.size):
                        for j in range(grid.size):
                                v = grid.map[i / 3][j]
                                if i % 3 == 1:
                                        string = str(v).center(7, ' ')
                                else:
                                        string = ' '
                                print(cTemp %  (colorMap[v], string))
                        print("")
                        if i % 3 == 2:
                                print("")
