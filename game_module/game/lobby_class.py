import pygame
from game_constants import *
import random
class Button:
    def __init__(self, x, y, w, h, text,color,hoverColor,action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.color = color
        self.hoverColor = hoverColor
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        font = pygame.font.SysFont(None, BUTTON_FONT_SIZE)
        color = self.color
        #change color on hover
        if self.rect.collidepoint(mouse_pos):
            color = self.hoverColor

        pygame.draw.rect(screen, color, self.rect)
        #border
        pygame.draw.rect(screen, BLACK, self.rect, BUTTON_BORDER_SIZE)

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  #clicks left click
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.action()
from game_module.game_server.server_constants import MAX_PLAYERS
class Lobby:
    def __init__(self,screen,sec,sock,addr):
        self.screen = screen
        self.buttons = []
        self.rooms_data = []
        self.refresh_button = Button(REFRESH_BUTTON_x, REFRESH_BUTTON_y, REFRESH_BUTTON_WIDTH, REFRESH_BUTTON_HEIGHT,"Refresh",GREY,HOVER_GREY,self.refresh_rooms)
        self.sock = sock
        self.addr = addr
        self.sec = sec
    def set_rooms(self, rooms_data):
        self.rooms_data = rooms_data
        self.build_room_buttons()

    def build_room_buttons(self):
        self.buttons = []
        for i, room in enumerate(self.rooms_data[:MAX_ROOMS]):  # max 14 rooms
            room_id, players = room
            col = i // ROOMS_PER_COLUMN
            row = i % ROOMS_PER_COLUMN
            x = COLUMN1_X + col * COLUMN_SPACE
            y = JOIN_START_Y + row * JOIN_Y_SPACING
            btn = Button(x,y,JOIN_BUTTON_WIDTH,JOIN_BUTTON_HEIGHT,f"Room {room_id} {players}/{MAX_PLAYERS}",GREEN,HOVER_GREEN,lambda r=room_id: self.join_room(r))

            self.buttons.append(btn)


    def refresh_rooms(self):
        msg = self.sec.encrypt("ROMS\x1E".encode())
        msg = b'ENCR'+msg
        self.sock.sendto(msg,self.addr)

    def join_room(self, room_id):
        msg = self.sec.encrypt(f"JOIN\x1E{room_id}".encode())
        msg = b'ENCR' + msg
        self.sock.sendto(msg, self.addr)
    def handle_buttons(self, event):
        self.refresh_button.handle_event(event)

        for b in self.buttons:
            b.handle_event(event)
    def handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
            self.handle_buttons(event)

    def draw(self):
        self.screen.fill(LOBBY_BACKGROUND_COLOR)

        self.refresh_button.draw(self.screen)

        for b in self.buttons:
            b.draw(self.screen)
import pygame
from game_constants import *
from game_module.game_server.server_constants import MAX_PLAYERS
import pygame
from game_constants import *
from game_module.game_server.server_constants import MAX_PLAYERS

class Waiting:
    def __init__(self, screen, room_id, sec, sock, addr):
        self.screen = screen
        self.room_id = room_id
        self.max_players = MAX_PLAYERS

        self.sock = sock
        self.addr = addr
        self.sec = sec

        self.player_count = 0
        self.ready_count = 0

        self.is_ready = False

        self.leave_button = Button(LEAVE_BUTTON_X, WAITING_TOP_PADDING,LEAVE_W, LEAVE_H,"Leave",LEAVE_COLOR,LEAVE_HOVER_COLOR,self.leave)

        self.ready_button = Button(SCREEN_X // 2 - READY_BUTTON_PADDING,SCREEN_Y - READY_BUTTON_PADDING,READY_W, READY_H,"Ready",READY_COLOR,READY_HOVER_COLOR,self.ready)

        self.font_big = pygame.font.SysFont(None, WAITING_BIG_SIZE)
        self.font = pygame.font.SysFont(None, WAITING_SIZE)


    def leave(self):
        self.is_ready = False
        msg = self.sec.encrypt(b"LEAV\x1E")
        self.sock.sendto(b"ENCR" + msg, self.addr)

    def ready(self):
        self.is_ready = not self.is_ready

        state = "1" if self.is_ready else "0"
        msg = self.sec.encrypt(f"REDY\x1E{state}".encode())
        self.sock.sendto(b"ENCR" + msg, self.addr)


    def setId(self, room_id):
        self.room_id = room_id

    def update_room_count(self, room_id, count):
        self.room_id = room_id
        self.player_count = int(count)

    def update_ready_count(self, count):
        self.ready_count = int(count)

    def handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False

            self.leave_button.handle_event(event)
            self.ready_button.handle_event(event)


    def draw(self):
        self.screen.fill(WAITING_BACKGROUND_COLOR)

        title = self.font_big.render(f"Room {self.room_id}",True,WHITE)
        self.screen.blit(title,((SCREEN_X // 2) - title.get_width() // 2, WAITING_TOP_PADDING))

        players_text = self.font.render("Players:", True, WAITING_PLAYER_COLOR)
        self.screen.blit(players_text, (WAITING_PLAYER_X, WAITING_PLAYER_STARTING_Y))

        status_text = self.font.render(f"Ready: {self.ready_count}/{self.player_count}",True,READY_COUNT_COLOR)
        self.screen.blit(status_text,(SCREEN_X // 2 - status_text.get_width() // 2, READY_COUNT_Y))

        if self.is_ready:
            self.ready_button.color = READY_COLOR
            self.ready_button.hoverColor = READY_HOVER_COLOR
            self.ready_button.text = "Ready"
        else:
            self.ready_button.color = UNREADY_COLOR
            self.ready_button.hoverColor = UNREADY_HOVER_COLOR
            self.ready_button.text = "Unready"

        self.leave_button.draw(self.screen)
        self.ready_button.draw(self.screen)