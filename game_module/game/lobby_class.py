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

class Lobby:
    def __init__(self,screen):
        self.screen = screen
        self.buttons = []
        self.rooms_data = []
        self.refresh_button = Button(REFRESH_BUTTON_x, REFRESH_BUTTON_y, REFRESH_BUTTON_WIDTH, REFRESH_BUTTON_HEIGHT,"Refresh",GREY,HOVER_GREY,self.refresh_rooms)

    def set_rooms(self, rooms_data):
        self.rooms_data = rooms_data
        self.build_room_buttons()

    def build_room_buttons(self):
        self.buttons = []
        for i, room in enumerate(self.rooms_data[:MAX_ROOMS]):  # max 14 rooms
            room_id, players, max_players = room
            col = i // ROOMS_PER_COLUMN
            row = i % ROOMS_PER_COLUMN
            x = COLUMN1_X + col * COLUMN_SPACE
            y = JOIN_START_Y + row * JOIN_Y_SPACING
            btn = Button(x,y,JOIN_BUTTON_WIDTH,JOIN_BUTTON_HEIGHT,f"Room {room_id} {players}/{max_players}",GREEN,HOVER_GREEN,lambda r=room_id: self.join_room(r))

            self.buttons.append(btn)


    def refresh_rooms(self):
        print("Requesting rooms from server...")

    def join_room(self, room_id):
        print(f"Joining room {room_id}")
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
        self.screen.fill((40, 40, 40))

        self.refresh_button.draw(self.screen)

        for b in self.buttons:
            b.draw(self.screen)
