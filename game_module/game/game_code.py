#imports
import pygame
from game_constants import *

#functions

def timer():
    pass
def print_board(board):
    [print(i) for i in board]
def draw_board(screen,board,x,y):
    xi = x
    for i in board:
        for j in i:
            if j == '':
                pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
            if j == 'R':
                pygame.draw.rect(screen, RED, (x, y, SQUARE_LEN, SQUARE_LEN))
                pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
            if j == 'G':
                pygame.draw.rect(screen, GREEN, (x, y, SQUARE_LEN, SQUARE_LEN))
                pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
            if j == 'B':
                pygame.draw.rect(screen, BLUE, (x, y, SQUARE_LEN, SQUARE_LEN))
                pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
            if j == 'Y':
                pygame.draw.rect(screen, YELLOW, (x, y, SQUARE_LEN, SQUARE_LEN))
                pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
            x += SQUARE_LEN
        y += SQUARE_LEN
        x= xi

#initialize

pygame.init()

screen = pygame.display.set_mode((SCREEN_X,  SCREEN_Y))

running = True

board = [[''] * BOARD_X_LEN for i in range(BOARD_Y_LEN)]

x=BOARD_X_START
y=BOARD_Y_START

#game loop
while running:
    screen.fill(WHITE)
    draw_board(screen,board,x,y)
    pygame.display.flip()
    #close the game when the X button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
