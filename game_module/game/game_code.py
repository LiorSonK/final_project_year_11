#imports
import time

import pygame
from game_constants import *
from game_classes import Status
from game_classes import Game
from game_classes import Draw
from lobby_class import Lobby
from lobby_class import Waiting
import threading
from login_module.login_interface.login_gui import SecureSession
from login_module.login_server.loginServer import handle_client

def handle_game(addr,aes,socket):
    #initialize
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X,  SCREEN_Y))
    Sec = SecureSession(aes)
    game = Game(screen,Sec,socket,addr)
    clock = pygame.time.Clock()
    lobby = Lobby(screen,Sec,socket,addr)
    waiting_lobby = Waiting(screen, -1,Sec,socket,addr)
    t = threading.Thread(target=handle_listen, args=(Sec,socket,game,lobby,waiting_lobby), daemon=True)
    t.start()
    #game loop
    while game.running:
        match game.gamestate:
            case Status.LOBBY:
                lobby.handle_events(game)
                lobby.draw()
                pygame.display.flip()
            case Status.WAITING_FOR_PLAYERS:
                waiting_lobby.draw()
                waiting_lobby.handle_events(game)
                pygame.display.flip()
            case Status.COUNTDOWN:
                game.COUNTDOWN_draw()
                gamestate = Status.INGAME
            case Status.INGAME:
                game.INGAME_draw()
                game.INGAME_handle_events()
            case Status.COMPLETED:
                pass
        clock.tick(FPS)
    t.join()
    pygame.quit()
def handle_listen(Sec,sock,game,lobby,waiting_lobby):
    sock.settimeout(0.5)
    while game.running:
        try:
            data,addr = sock.recvfrom(1024)
            data = Sec.decrypt(data).decode()
            code = data.split('\x1E')[0]
            if code == 'RMDT':
                info = data.split('\x1E')[1]
                info = info.split('|')
                rooms_data = []
                for i in info:
                    if(len(i)>0):
                        i = i.split('\n')
                        id = i[0]
                        player_count = i[2]
                        rooms_data.append((id.split(':')[1].strip(),player_count.split(':')[1].strip()))
                lobby.set_rooms(rooms_data)
            if code == 'JOND':
                id = data.split('\x1E')[1]
                waiting_lobby.setId(id)
                game.gamestate = Status.WAITING_FOR_PLAYERS
            if code == 'LEFT':
                waiting_lobby.setId(-1)
                game.gamestate = Status.LOBBY
            if code == 'CLOS':
                game.gamestate = Status.LOBBY
                game.color = None
                game.room = None
                game.reset_board()
                lobby.set_rooms([])
                waiting_lobby.setId(-1)
            if code == 'PLCN':
                room_id = data.split('\x1E')[1]
                count = data.split('\x1E')[2]

                waiting_lobby.update_room_count(room_id, count)
            if code == "RDYC":
                room_id = data.split('\x1E')[1]
                ready_count = data.split('\x1E')[2]
                waiting_lobby.update_ready_count(int(ready_count))
            if code == 'STRT':
                room_id = data.split('\x1E')[1]
                game.color = data.split('\x1E')[2].upper()
                x = int(data.split('\x1E')[3])
                y = int(data.split('\x1E')[4])
                game.board[y][x] = game.color
                if room_id == waiting_lobby.room_id:
                    game.gamestate = Status.INGAME
            if code == 'CNGE':
                letter = data.split('\x1E')[1]
                x = int(data.split('\x1E')[2])
                y = int(data.split('\x1E')[3])
                game.board[y][x] = letter
            if code == 'MOVD':
                old_x = int(data.split('\x1E')[1])
                old_y = int(data.split('\x1E')[2])
                x = int(data.split('\x1E')[3])
                y = int(data.split('\x1E')[4])
                color = data.split('\x1E')[5]
                game.board[old_y][old_x] = color.upper()
                game.board[y][x] = color.lower()
        except TimeoutError:
            pass
    sock.close()

