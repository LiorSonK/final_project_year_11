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
    def __init__(self):
        self.buttons = []
        self.rooms_data = []
        self.refresh_button = Button(REFRESH_BUTTON_x, REFRESH_BUTTON_y, REFRESH_BUTTON_WIDTH, REFRESH_BUTTON_HEIGHT,"Refresh",GREY,HOVER_GREY,self.refresh_rooms)

    def set_rooms(self, rooms_data):
        self.rooms_data = rooms_data
        self.build_room_buttons()

    def build_room_buttons(self):
        self.buttons = []
        column1 = COLUMN1_X
        column2 = COLUMN2_X  # column 2
        y_start = JOIN_START_Y
        spacing = JOIN_Y_SPACING
        for i, room in enumerate(self.rooms_data[:MAX_ROOMS]):  # max 14 rooms
            room_id, players, max_players = room
            if i < MAX_ROOMS/2:
                x = column1
                y = y_start + i * spacing
            else:
                x = column2
                y = y_start + (i - MAX_ROOMS/2) * spacing
            btn = Button(x,y,JOIN_BUTTON_WIDTH,JOIN_BUTTON_HEIGHT,f"Room {room_id} {players}/{max_players}",GREEN,HOVER_GREEN,lambda r=room_id: self.join_room(r))

            self.buttons.append(btn)

    def refresh_rooms(self):
        print("Requesting rooms from server...")

    def join_room(self, room_id):
        print(f"Joining room {room_id}")

    def handle_events(self, event):
        self.refresh_button.handle_event(event)

        for b in self.buttons:
            b.handle_event(event)

    def draw(self, screen):
        screen.fill((40, 40, 40))

        self.refresh_button.draw(screen)

        for b in self.buttons:
            b.draw(screen)


pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fake_rooms = [
    (101, 0, 8),   # empty lobby
    (102, 1, 8),   # just started
    (103, 6, 8),   # mid game
    (104, 8, 8),   # full room
    (105, 3, 4),   # small match
    (106, 10, 10), # full
    (107, 2, 6),
    (108, 5, 6),
    (109, 1, 2)
]
lobby = Lobby()
lobby.set_rooms(fake_rooms)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        lobby.handle_events(event)

    lobby.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()