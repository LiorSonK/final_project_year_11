#imports
import pygame
from game_constants import *
from game_classes import Status
from game_classes import Game
from game_classes import Draw

#initialize
pygame.init()

screen = pygame.display.set_mode((SCREEN_X,  SCREEN_Y))

color = 'R'
cr = ['R','G','B','Y','r']
game = Game(screen,color)
gamestate = Status.COUNTDOWN
#game loop
while game.running:
    match gamestate:
        case Status.WAITING_FOR_PLAYERS:
            pass
        case Status.COUNTDOWN:
            game.COUNTDOWN_draw()
            gamestate = Status.INGAME
        case Status.INGAME:
            game.INGAME_draw()
            game.INGAME_handle_events()
        case Status.COMPLETED:
            pass

pygame.quit()