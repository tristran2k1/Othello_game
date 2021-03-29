import pygame
import os
import random
import numpy as np
import ctypes
from pygame.locals import *
pygame.init()
WINDOWSWIDTH = 960
WINDOWSHEIGHT = 640
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
GREEN = (0, 37, 41)
ROSE = (235, 52, 195)
RED = (245, 66, 66)
BLACK = (0, 0, 0)
FPS = 60
FPSClock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textsurface1 = myfont.render('Black Score: ', False, BLACK)
textsurface2= myfont.render('White Score: ', False, WHITE)
class GUI:
    def __init__(self, cell, victory_cell):
        self.Screen = pygame.display.set_mode((WINDOWSWIDTH, WINDOWSHEIGHT))
        pygame.display.set_caption('Othello by @T team')
        self.Screen.fill(GREY)
        pygame.draw.rect(self.Screen, GREEN, pygame.Rect(50, 50, 530, 530))
        x1 = 57
        x2 = 57
        y = 65
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.Screen, BLACK, pygame.Rect(x1 + (j * 64), x2, y, y), 2)
            x2 = x2 + 64
        self.Screen.blit(textsurface1, (600, 100))
        self.Screen.blit(textsurface2, (600, 500))
        self.board = cell
        self.victoryCell = victory_cell
    def getVictoryCell(self, x, y):
        pygame.draw.rect(self.Screen, RED, pygame.Rect(59 + (x * 64), 59 + (y * 64), 62, 62))
    def scoreUpdate(self, bScore, wScore):
        pygame.draw.rect(self.Screen, GREY, pygame.Rect(800, 100, 100, 100))
        pygame.draw.rect(self.Screen, GREY, pygame.Rect(800, 500, 100, 100))
        blackScore = str(bScore)
        whiteScore = str(wScore)
        textsurface = myfont.render(blackScore, False, BLACK)
        self.Screen.blit(textsurface, (800, 100))
        textsurface = myfont.render(whiteScore, False, WHITE)
        self.Screen.blit(textsurface, (800, 500))
    def display(self, board, position):
        temp = list(position)
        bScore = 0
        wScore = 0
        for i in range(8):
            for j in range(8):
                if board[i,j] == 'B':
                    pygame.draw.circle(self.Screen, BLACK, temp, 20)
                    bScore += 1
                elif board[i,j] == 'W':
                    pygame.draw.circle(self.Screen, WHITE, temp, 20)
                    wScore += 1
                temp[0] = temp[0] + 64
            temp[0] = position[0]
            temp[1] = temp[1] + 64
        self.scoreUpdate(bScore, wScore)
    def drawVictoryCell(self):
        for i in range(5):
            self.getVictoryCell(self.victoryCell[0][i],self.victoryCell[1][i])
    def run(self, winner):
        if winner is not None:
            count = 1
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                    self.display(self.board, (90, 90))
                    pygame.display.flip()
                    if count == 1:
                        ctypes.windll.user32.MessageBoxW(0,"The winner is:  " + winner, "Congratulation !!", 1)
                        count -= 1
                    FPSClock.tick(FPS)
        else:
            self.display(self.board, (90, 90))
            pygame.display.flip()
            FPSClock.tick(FPS)




