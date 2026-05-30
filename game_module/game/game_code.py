#imports
import pygame
from game_constants import *
from game_classes import Status
from game_classes import Game
from game_classes import Draw
from lobby_class import Lobby

#initialize
pygame.init()

screen = pygame.display.set_mode((SCREEN_X,  SCREEN_Y))

color = 'R'
cr = ['R','G','B','Y','r']
game = Game(screen,color)
gamestate = Status.LOBBY
clock = pygame.time.Clock()
fake_rooms = [
    (101, 0, 8),  # empty lobby
    (102, 1, 8),  # just started
    (103, 6, 8),  # mid game
    (104, 8, 8),  # full room
    (105, 3, 4),  # small match
    (106, 10, 10),  # full
    (107, 2, 6),
    (108, 5, 6),
    (109, 1, 2),
    (101, 0, 8),  # empty lobby
    (102, 1, 8),  # just started
    (103, 6, 8),  # mid game
    (104, 8, 8),  # full room
    (105, 3, 4),  # small match
    (106, 10, 10),  # full
    (107, 2, 6),
    (108, 5, 6),
    (109, 1, 2),
    (101, 0, 8),  # empty lobby
    (102, 1, 8),  # just started
    (103, 6, 8),  # mid game
    (104, 8, 8),  # full room
    (105, 3, 4),  # small match
    (106, 10, 10),  # full
    (107, 2, 6),
    (108, 5, 6),
    (109, 1, 2),
    (101, 0, 8),  # empty lobby
    (102, 1, 8),  # just started
    (103, 6, 8),  # mid game
    (104, 8, 8),  # full room
    (105, 3, 4),  # small match
    (106, 10, 10),  # full
    (107, 2, 6),
    (108, 5, 6),
    (109, 1, 2),
]
lobby = Lobby(screen)
lobby.set_rooms(fake_rooms)

#game loop
while game.running:
    match gamestate:
        case Status.LOBBY:
            lobby.handle_events(game)
            lobby.draw()
            pygame.display.flip()
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
    clock.tick(FPS)
pygame.quit()