import pygame
from game_constants import *
from enum import Enum
import random
import time



class Game:
    def __init__(self, screen, color):
        self.running = True
        self.board = [[''] * BOARD_X_LEN for _ in range(BOARD_Y_LEN)]
        self.color = color
        self.screen = screen

        self.drawer = Draw(self.board, self.color, self.screen)

    def INGAME_handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_SPACE:
                    self.board[random.randint(1, 29)][random.randint(1, 29)] = \
                        random.choice(['R', 'G', 'B', 'Y'])

    def INGAME_draw(self):
        self.drawer.draw_ingame()

    def COUNTDOWN_draw(self):
        clock = pygame.time.Clock()

        for i in range(3):
            start_time = pygame.time.get_ticks()

            while pygame.time.get_ticks() - start_time < 1000:
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        self.running = False
                        return

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                            return

                self.screen.fill(WHITE)
                self.drawer.draw_big(str(3 - i), CD_X, CD_Y)
                pygame.display.flip()
                clock.tick(60)

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 500:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            self.screen.fill(WHITE)
            self.drawer.draw_big("Go!", CD_X - CD_GO_OFFSET, CD_Y)
            pygame.display.flip()
            clock.tick(60)


class Draw:
    def __init__(self,board,color,screen):
        self.board = board
        self.color = color
        self.rgby = (0,0,0,0) #game starts with no colors (although technicly it has colors, but it updates after only a few ms so it doesn't matter)
        self.screen = screen
    def draw_title(self):
        title_font = pygame.font.SysFont(None, TITLE_SIZE)
        title_text = title_font.render("Lior's Game", True, BLACK)
        self.screen.blit(title_text, (TITLE_X, TITLE_Y))
    def count_board(self):
        r, g, b, y = 0, 0, 0, 0
        for i in self.board:
            for j in i:
                if j == 'R' or j == 'r':
                    r += 1
                if j == 'G' or j == 'g':
                    g += 1
                if j == 'B' or j == 'b':
                    b += 1
                if j == 'Y' or j == 'y':
                    y += 1
        self.rgby = (r, g, b, y)

    def draw_statistics(self):
        title_font = pygame.font.SysFont(None, STATISTICS_TITLE_SIZE)
        title_text = title_font.render("STATISTICS", True, BLACK)

        statistics_font = pygame.font.SysFont(None, STATISTIC_SIZE)
        #count board needs to be called in order for rgby to update
        self.count_board()
        total_colored = sum(self.rgby)
        total_left = (BOARD_X_LEN * BOARD_Y_LEN) - total_colored

        self.screen.blit(statistics_font.render(f'The color red has: {self.rgby[0]}', True, RED),
                    (STATISTICS_TITLE_X, STATISTICS_TITLE_Y + STATISTIC_Y_OFFSET))
        self.screen.blit(statistics_font.render(f'The color green has: {self.rgby[1]}', True, GREEN),
                    (STATISTICS_TITLE_X, STATISTICS_TITLE_Y + STATISTIC_Y_OFFSET * 1.5))
        self.screen.blit(statistics_font.render(f'The color blue has: {self.rgby[2]}', True, BLUE),
                    (STATISTICS_TITLE_X, STATISTICS_TITLE_Y + STATISTIC_Y_OFFSET * 2))
        self.screen.blit(statistics_font.render(f'The color yellow has: {self.rgby[3]}', True, YELLOW),
                    (STATISTICS_TITLE_X, STATISTICS_TITLE_Y + STATISTIC_Y_OFFSET * 2.5))
        self.screen.blit(statistics_font.render(f'total colored: {total_colored}', True, BLACK),
                    (STATISTICS_TITLE_X, STATISTICS_TITLE_Y + STATISTIC_Y_OFFSET * 3))
        self.screen.blit(statistics_font.render(f'total left: {total_left}', True, BLACK),
                    (STATISTICS_TITLE_X, STATISTICS_TITLE_Y + STATISTIC_Y_OFFSET * 3.5))
        self.screen.blit(title_text, (STATISTICS_TITLE_X, STATISTICS_TITLE_Y))

    def timer(self):
        pass

    def print_board(self):
        [print(i) for i in self.board]

    def draw_board(self):
        x = BOARD_X_START
        y = BOARD_Y_START
        xi = x
        font = pygame.font.SysFont(None, PLAYER_TEXT_SIZE)
        text = font.render("U", True, BLACK)
        for i in self.board:
            for j in i:
                # land cubes
                if j == '':
                    pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                if j == 'R':
                    pygame.draw.rect(self.screen, RED, (x, y, SQUARE_LEN, SQUARE_LEN))
                    pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                if j == 'G':
                    pygame.draw.rect(self.screen, GREEN, (x, y, SQUARE_LEN, SQUARE_LEN))
                    pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                if j == 'B':
                    pygame.draw.rect(self.screen, BLUE, (x, y, SQUARE_LEN, SQUARE_LEN))
                    pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                if j == 'Y':
                    pygame.draw.rect(self.screen, YELLOW, (x, y, SQUARE_LEN, SQUARE_LEN))
                    pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                # player cube
                if j == 'r':
                    if self.color == 'R':
                        pygame.draw.rect(self.screen, RED, (x, y, SQUARE_LEN, SQUARE_LEN))
                        self.screen.blit(text, (x + PLAYER_TEXT_OFFSET_X, y + PLAYER_TEXT_OFFSET_Y))
                        pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                    else:
                        pygame.draw.rect(self.screen, RED, (x, y, SQUARE_LEN, SQUARE_LEN))
                        pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                if j == 'g':
                    if self.color == 'G':
                        pygame.draw.rect(self.screen, GREEN, (x, y, SQUARE_LEN, SQUARE_LEN))
                        self.screen.blit(text, (x + PLAYER_TEXT_OFFSET_X, y + PLAYER_TEXT_OFFSET_Y))
                        pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                    else:
                        pygame.draw.rect(self.screen, GREEN, (x, y, SQUARE_LEN, SQUARE_LEN))
                        pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                if j == 'b':
                    if self.color == 'B':
                        pygame.draw.rect(self.screen, BLUE, (x, y, SQUARE_LEN, SQUARE_LEN))
                        self.screen.blit(text, (x + PLAYER_TEXT_OFFSET_X, y + PLAYER_TEXT_OFFSET_Y))
                        pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                    else:
                        pygame.draw.rect(self.screen, BLUE, (x, y, SQUARE_LEN, SQUARE_LEN))
                        pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                if j == 'y':
                    if self.color == 'Y':
                        pygame.draw.rect(self.screen, YELLOW, (x, y, SQUARE_LEN, SQUARE_LEN))
                        self.screen.blit(text, (x + PLAYER_TEXT_OFFSET_X, y + PLAYER_TEXT_OFFSET_Y))
                        pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                    else:
                        pygame.draw.rect(self.screen, YELLOW, (x, y, SQUARE_LEN, SQUARE_LEN))
                        pygame.draw.rect(self.screen, BLACK, (x, y, SQUARE_LEN, SQUARE_LEN), BORDER_WIDTH)
                x += SQUARE_LEN
            y += SQUARE_LEN
            x = xi
    def draw_ingame(self):
        self.screen.fill(WHITE)
        self.draw_board()
        self.draw_statistics()
        self.draw_title()
        pygame.display.flip()
    def draw_big(self,txt,x,y):
        font = pygame.font.SysFont(None, CD_SIZE)
        text = font.render(txt, True, BLACK)
        self.screen.blit(text, (x,y))

class Status(Enum):
    WAITING_FOR_PLAYERS = 0
    COUNTDOWN = 1
    INGAME = 2
    COMPLETED = 3
