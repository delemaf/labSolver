#!/usr/bin/python

import sys

class Dijkstra:
    def __init__(self, maze):
        self.maze = maze
        self.it = 1
        y = x = 0
        for line in self.maze:
            for e in line:
                if e == 'D':
                    self.ghost = {'x': x, 'y': y}
                x = x + 1
            y = y + 1
            x = 0
        self.place(self.ghost['y'], self.ghost['x'])
        self.it += 1
        self.move()
    
    def place(self, x, y):
        if self.maze[x + 1][y] == 'A' or self.maze[x - 1][y] == 'A' \
           or self.maze[x][y + 1] == 'A' or self.maze[x][y - 1] == 'A':
            self.it -= 1
            self.maze[x][y] = '(' + str(self.it) + ')'
            self.trace(x, y)
            return 0
        if self.maze[x + 1][y] == 'O':
            self.maze[x + 1][y] = str(self.it)
        if self.maze[x - 1][y] == 'O':
            self.maze[x - 1][y] = str(self.it)
        if self.maze[x][y + 1] == 'O':
            self.maze[x][y + 1] = str(self.it)
        if self.maze[x][y - 1] == 'O':
            self.maze[x][y - 1] = str(self.it)
        return 1

    def move(self):
        y = x = 0
        for line in self.maze:
            for e in line:
                if e == str(self.it - 1):
                    if self.place(y, x) == 0: return self.it - 1  
                x += 1
            y += 1
            x = 0
        self.it += 1
        self.move()

    def trace(self, x, y):
        self.it -= 1
        if self.it == 0:
            return 0            
        if self.maze[x + 1][y] == str(self.it):
            self.maze[x + 1][y] = '(' + str(self.it) + ')'
            x += 1
        if self.maze[x - 1][y] == str(self.it):
            self.maze[x - 1][y] = '(' + str(self.it) + ')'
            x -= 1
        if self.maze[x][y + 1] == str(self.it):
            self.maze[x][y + 1] = '(' + str(self.it) + ')'
            y += 1
        if self.maze[x][y - 1] == str(self.it):
            self.maze[x][y - 1] = '(' + str(self.it) + ')'        
            y -= 1
        self.trace(x, y)
