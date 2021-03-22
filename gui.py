import pygame
import os
import random
import numpy as np
from pygame.locals import *

def GUI(cell, victory_cell):
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
    Screen = pygame.display.set_mode((WINDOWSWIDTH, WINDOWSHEIGHT))
    pygame.display.set_caption('Othello by @Song cho hom nay mai chet cung duoc')
    Screen.fill(GREY)
    pygame.draw.rect(Screen, GREEN, pygame.Rect(50, 50, 530, 530))
    x1 = 57
    x2 = 57
    y = 65
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(Screen, BLACK, pygame.Rect(x1 + (j * 64), x2, y, y), 2)
        x2 = x2 + 64
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('Score: ', False, WHITE)
    Screen.blit(textsurface, (600, 100))
    Screen.blit(textsurface, (600, 500))
    ####board = np.array([['W'] * 8] * 8)
    board = cell
    def getVictoryCell(x, y):
        pygame.draw.rect(Screen, RED, pygame.Rect(59 + (x * 64), 59 + (y * 64), 62, 62))

    def scoreUpdate(bScore, wScore):
        pygame.draw.rect(Screen, GREY, pygame.Rect(700, 100, 100, 100))
        pygame.draw.rect(Screen, GREY, pygame.Rect(700, 500, 100, 100))
        blackScore = str(bScore)
        whiteScore = str(wScore)
        textsurface = myfont.render(blackScore, False, ROSE)
        Screen.blit(textsurface, (700, 100))
        textsurface = myfont.render(whiteScore, False, ROSE)
        Screen.blit(textsurface, (700, 500))

    def display(board, position):
        temp = list(position)
        bScore = 0
        wScore = 0
        for i in range(8):
            for j in range(8):
                if board[i,j] == 'B':
                    pygame.draw.circle(Screen, BLACK, temp, 20)
                    bScore += 1
                elif board[i,j] == 'W':
                    pygame.draw.circle(Screen, WHITE, temp, 20)
                    wScore += 1
                else:
                    pygame.draw.circle(Screen, GREEN, temp, 20)
                temp[0] = temp[0] + 64
            temp[0] = position[0]
            temp[1] = temp[1] + 64
        scoreUpdate(bScore, wScore)

    for i in range(5):
        getVictoryCell(victory_cell[0][i],victory_cell[1][i])

    mylist = ["B", "W", "E"]
    """while True:
        mouseClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                display(board, (90, 90))
                for i in range(8):
                    for j in range(8):
                        board[i,j] = random.choice(mylist)

        pygame.display.flip()
        FPSClock.tick(FPS)"""
    display(board, (90, 90))
    pygame.display.flip()
    FPSClock.tick(FPS)




