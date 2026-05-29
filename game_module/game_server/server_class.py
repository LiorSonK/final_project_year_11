import socket
import json

from game_module.game.game_constants import BOARD_X_LEN, BOARD_Y_LEN
from server_constants import *
from game_module.game.game_classes import Status
import time

class Server:
    def __init__(self,ip,port):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind((ip,port))
        self.shutdown = False
        self.playerCount = 0
        self.rooms = {}
        self.players = {}
    def handle_msg(self,data,addr):
        msg = data.decode()
        cmd = msg[:4]

        if addr not in self.players:
            self.players[addr] = {"username": "unknown","room": None}
            self.playerCount+=1
        player = self.players[addr]

        if cmd == "LIST":
            rooms_data = []
            for r in self.rooms.values():
                rooms_data.append(f"{r.room_id},{len(r.players)}/{r.max_players}")

            self.socket.sendto(("ROOMS|" + ";".join(rooms_data)).encode(),addr)

        elif cmd == "JOIN":
            room_id = int(msg[5:])
            if player["room"] is not None:
                old = self.rooms[player["room"]]
                if addr in old.players:
                    old.remove_player(addr)

            room = self.rooms[room_id]
            room.add_player(addr,player["username"])
            player["room"] = room_id

            self.socket.sendto(f"JOIN_OK|{room_id}".encode(),addr)
            self.broadcast_room(room_id, f"PLAYER_JOIN|{addr}")

        elif cmd == "LEAV":
            if player["room"] is not None:
                room = self.rooms[player["room"]]
                room.remove_player(addr)
                self.broadcast_room(player["room"], f"PLAYER_LEAVE|{addr}")
                player["room"] = None
            self.socket.sendto(b"LEFT", addr)
        elif cmd == "BORD":
            if player["room"] is None:
                self.socket.sendto(b"ERR|NO_ROOM", addr)
                return
            room = self.rooms[player["room"]]
            msg = "BOARD|" + json.dumps(room.board)
            self.socket.sendto(msg.encode(), addr)

        elif cmd == "MOVE":

            if player["room"] is None:
                return

            direction = msg[5:]
            room = self.rooms[player["room"]]
            room_player = room.players[addr]
            color = room_player["color"]
            self.broadcast_room(player["room"],f"POS|{color.lower()}|{room_player['x']}|{room_player['y']}")

            if direction == "UP":
                room_player["y"] -= 1
            elif direction == "DOWN":
                room_player["y"] += 1
            elif direction == "LEFT":
                room_player["x"] -= 1
            elif direction == "RIGHT":
                room_player["x"] += 1

            self.broadcast_room(player["room"],f"POS|{color.upper()}|{room_player['x']}|{room_player['y']}")

    def broadcast_room(self, room_id, msg):
        room = self.rooms[room_id]

        for addr in room.players:
            self.socket.sendto(msg.encode(), addr)

    def start_rooms(self):
        for i in range(5):
            self.rooms[i] = Room(i)

    def add_room(self):
        if len(self.rooms)<9:
            self.rooms[len(self.rooms)] = Room(len(self.rooms))

    def print_rooms(self):
        for i in self.rooms:
            print(i)

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.max_players = MAX_PLAYERS
        self.players = {}
        self.started = False
        self.board = []
        self.colors_left = ['r', 'g', 'b', 'y']

        self.state = Status.WAITING_FOR_PLAYERS
        self.state_start_time = time.time()
    def update_state(self):

        if self.state == Status.WAITING_FOR_PLAYERS:
            if len(self.players) >= 2:
                self.state = Status.COUNTDOWN
                self.state_start_time = time.time()

        elif self.state == Status.COUNTDOWN:

            elapsed = time.time() - self.state_start_time

            if elapsed >= 3:
                self.state = Status.INGAME

        elif self.state == Status.INGAME:

            if len(self.players) == 0:
                self.state = Status.COMPLETED

        elif self.state == Status.COMPLETED:

            self.reset_room()
            self.state = Status.WAITING_FOR_PLAYERS

    def broadcast(self, socket, msg):

        for addr in self.players:
            socket.sendto(msg.encode(), addr)

    def broadcast_state(self, socket):

        self.broadcast(socket, f"STATE|{self.state.name}")
    def reset_room(self):
        self.players = {}
        self.started = False
        self.board = [[''] * BOARD_X_LEN for _ in range(BOARD_Y_LEN)]
        self.colors_left = ['r', 'g', 'b', 'y']

    def add_player(self, addr, username):
        color = self.colors_left.pop(0)
        self.players[addr] = {
            "color": color,
            "x": 0,
            "y": 0,
            "username": username
        }

    def remove_player(self, addr):
        if addr in self.players:
            color = self.players[addr]["color"]
            self.colors_left.append(color)
            del self.players[addr]

    def __str__(self):
        return f"Id: {self.room_id}\nStarted: {self.started}\nPlayerCount: {len(self.players)}"