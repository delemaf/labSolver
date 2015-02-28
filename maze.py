#!/usr/bin/python

import sys
import random
import time
import pygame
from pygame.locals import *

class Maze:
    def __init__(self):
        self.tmp = dict()

    def get(self):
        return self.maze

    def open(self, path):
        f = open(path, 'r')
        buf = f.read()
        f.close()
        if 'A' not in buf or 'D' not in buf:
            print 'Error: Missing Pacman or ghost in {0}.'.format(path)
            sys.exit(0)    
        if len(buf.strip('01DA\n')) == 0:
            buf = buf.replace('1', 'W')
            buf = buf.replace('0', 'O')
            buf = buf.splitlines()
            i = 0
            for l in buf:
                buf[i] = list(l)
                i += 1
            self.maze = buf
        else:
            print 'Error: Wrong character: {0}.'.format(buf.strip('01DA\n'))
            sys.exit(0)
        self.width = len(self.maze[0])
        self.height = len(self.maze)
        
    def dump(self):
        for line in self.maze:
            for e in line:
                if len(e) == 1:
                    if e == 'O':
                        sys.stdout.write('   ')                        
                    elif e == 'W':
                        sys.stdout.write('   ')
                    else:
                        sys.stdout.write(' ' + e + ' ')
                elif len(e) == 2:
                    sys.stdout.write(' ' + e)
                elif len(e) == 3:
                    sys.stdout.write(' ' + e[1:-1] + ' ')
                elif len(e) == 4:
                    sys.stdout.write(' ' + e[1:-1])
            sys.stdout.write('\n')

    def draw(self):
        self.maze = list()
        for y in range(0, self.height):
            tmp = list()
            for x in range(0, self.width):
                if self.tmp[x][y] == 1:
                    tmp.append('W')
                elif self.tmp[x][y] == 2:
                    tmp.append('A')
                elif self.tmp[x][y] == 3:
                    tmp.append('D')
                else:
                    tmp.append('O')
            self.maze.append(tmp)

    def init_tmp(self):
        for x in range(0, self.width):
            self.tmp[x] = dict()
            for y in range(0, self.height):
                self.tmp[x][y] = 1

    def carve(self, x, y):
        dir = random.randint(0, 3)
        count = 0
        while count < 4:
            dx = 0
            dy = 0
            if dir == 0:
                dx = 1
            elif dir == 1:
                dy = 1
            elif dir == 2:
                dx = -1
            else:
                dy = -1
            x1 = x + dx
            y1 = y + dy
            x2 = x1 + dx
            y2 = y1 + dy
            if x2 > 0 and x2 < self.width and y2 > 0 and y2 < self.height:
                if self.tmp[x1][y1] == 1 and self.tmp[x2][y2] == 1:
                    self.tmp[x1][y1] = 0
                    self.tmp[x2][y2] = 0
                    self.carve(x2, y2)
            count = count + 1
            dir = (dir + 1) % 4

    def gen(self, width, height):
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
        self.width = width
        self.height = height
        self.init_tmp()
        random.seed()
        self.carve(1, 1)
        startx = starty = endx = endy = 0
        while self.tmp[startx][starty]:
            startx = random.randint(1, self.width - 2)
            starty = random.randint(1, self.height - 2)
        while self.tmp[endx][endy] or endx == 0 or abs(startx - endx) < int(self.width / 3) \
              or abs(starty - endy) < int(self.height / 3):
            endx = random.randint(1, self.width - 2)
            endy = random.randint(1, self.height - 2)
        self.tmp[startx][starty] = 2
        self.tmp[endx][endy] = 3
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.draw()

    def graphic(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width * 32, self.height * 32))
        pygame.display.set_caption('304pacman') 
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        font = pygame.font.SysFont("monospace", 20)
        wall = pygame.image.load('img/wall.png')
        pacman = pygame.image.load('img/pacman.png')
        ghost = pygame.image.load('img/ghost.png')
        yellow = pygame.image.load('img/yellow.png')
        x = y = 0
        for line in self.maze:
            for e in line:
                if e == 'W':
                    screen.blit(wall, (x, y))
                elif e == 'A':
                    screen.blit(pacman, (x, y))                
                elif e == 'D':
                    screen.blit(ghost, (x, y))                
                elif e.isdigit() or e[1:-1].isdigit():
                    
                    if e[:1] == '(': 
                        screen.blit(yellow, (x, y))
                        e = e[1:-1]
                        label = font.render(e, 1, (0,0,0))
                    else:
                        label = font.render(e, 1, (255,255,255))
                    if len(e) == 1:
                        screen.blit(label, (x + 6, y + 6))
                    elif len(e) == 2:
                        screen.blit(label, (x, y + 6))
                    else:
                        screen.blit(label, (x - 2, y + 6))
                x = x + 32
            y = y + 32
            x = 0
        pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
