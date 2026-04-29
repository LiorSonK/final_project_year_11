#imports
import pygame
from game_constants import *
import random
#functions
def count_board(board):
    r,g,b,y=0,0,0,0
    for i in board:
        for j in i:
            if j =='R' or j == 'r':
                r+=1
            if j =='G' or j == 'g':
                g+=1
            if j =='B' or j == 'b':
                b+=1
            if j =='Y' or j == 'y':
                y+=1
    return r,g,b,y
def draw_statistics(rgby):
    title_font = pygame.font.SysFont(None,TITLE_SIZE)
    title_text = title_font.render("STATISTICS",True,BLACK)

    statistics_font = pygame.font.SysFont(None, STATISTIC_SIZE)
    total_colored = sum(rgby)
    total_left = (BOARD_X_LEN*BOARD_Y_LEN) - total_colored

    screen.blit(statistics_font.render(f'The color red has: {rgby[0]}',True,RED),
                (TITLE_X,TITLE_Y + STATISTIC_Y_OFFSET))
    screen.blit(statistics_font.render(f'The color green has: {rgby[1]}', True, GREEN),
                (TITLE_X, TITLE_Y + STATISTIC_Y_OFFSET*1.5))
    screen.blit(statistics_font.render(f'The color blue has: {rgby[2]}', True, BLUE),
                (TITLE_X, TITLE_Y + STATISTIC_Y_OFFSET*2))
    screen.blit(statistics_font.render(f'The color yellow has: {rgby[3]}', True, YELLOW),
                (TITLE_X, TITLE_Y + STATISTIC_Y_OFFSET*2.5))
    screen.blit(statistics_font.render(f'total colored: {total_colored}', True, BLACK),
                (TITLE_X, TITLE_Y + STATISTIC_Y_OFFSET * 3))
    screen.blit(statistics_font.render(f'total left: {total_left}', True, BLACK),
                (TITLE_X, TITLE_Y + STATISTIC_Y_OFFSET * 3.5))
    screen.blit(title_text,(TITLE_X,TITLE_Y))
def timer():
    pass
def print_board(board):
    [print(i) for i in board]
def draw_board(screen,board):
    x = BOARD_X_START
    y = BOARD_Y_START
    xi = x
    font = pygame.font.SysFont(None,PLAYER_TEXT_SIZE)
    text = font.render("U",True, BLACK)
    for i in board:
        for j in i:
            #land cubes
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
            #player cube
            if j == 'r':
                if color == 'R':
                    pygame.draw.rect(screen, RED, (x, y, SQUARE_LEN, SQUARE_LEN))
                    screen.blit(text,(x+PLAYER_TEXT_OFFSET_X,y+PLAYER_TEXT_OFFSET_Y))
                    pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                else:
                    pygame.draw.rect(screen, RED, (x, y, SQUARE_LEN, SQUARE_LEN))
                    pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
            if j == 'g':
                if color =='G':
                    pygame.draw.rect(screen, GREEN, (x, y, SQUARE_LEN, SQUARE_LEN))
                    screen.blit(text, (x + PLAYER_TEXT_OFFSET_X, y + PLAYER_TEXT_OFFSET_Y))
                    pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                else:
                    pygame.draw.rect(screen, GREEN, (x, y, SQUARE_LEN, SQUARE_LEN))
                    pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
            if j == 'b':
                if color=='B':
                    pygame.draw.rect(screen, BLUE, (x, y, SQUARE_LEN, SQUARE_LEN))
                    screen.blit(text, (x + PLAYER_TEXT_OFFSET_X, y + PLAYER_TEXT_OFFSET_Y))
                    pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                else:
                    pygame.draw.rect(screen, BLUE, (x, y, SQUARE_LEN, SQUARE_LEN))
                    pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
            if j == 'y':
                if color=='Y':
                    pygame.draw.rect(screen, YELLOW, (x, y, SQUARE_LEN, SQUARE_LEN))
                    screen.blit(text, (x + PLAYER_TEXT_OFFSET_X, y + PLAYER_TEXT_OFFSET_Y))
                    pygame.draw.rect(screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                else:
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

color = 'R'

cr = ['R','G','B','Y']
#game loop
while running:
    screen.fill(WHITE)
    draw_board(screen,board)
    draw_statistics(count_board(board))
    pygame.display.flip()
    #close the game when the X button/ESC key is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                board[random.randint(1,29)][random.randint(1,29)] = cr[random.randint(0,3)]

pygame.quit()
