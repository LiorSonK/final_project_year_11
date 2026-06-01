import socket
import json
from game_module.game.game_constants import BOARD_X_LEN, BOARD_Y_LEN
from server_constants import *
from game_module.game.game_classes import Status
import time
from login_module.login_server.loginServer import SecureSession
class Server:
    def __init__(self,ip,port):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind((ip,port))
        self.shutdown = False
        self.playerCount = 0
        self.rooms = []
        self.players = []
    def handle_msg(self,data,addr):
        msg = data
        encryption = msg[:4].decode()
        if encryption == "NOEN":
            msg = msg[4:].decode()
            cmd = msg.split('\x1E')[0]
            if cmd == "CONN":
                username = msg.split('\x1E')[1]
                for player in self.players:
                    if player.username == username:
                        player.addr = addr
                        self.socket.sendto(b"OK", addr)
                        return
        if encryption == "ENCR":
            player = self.find_player(addr)
            if player is None:
                print("JOIN FAILED: player not registered", addr)
                return
            secure = SecureSession(player.aes_key)

            msg = secure.decrypt(msg[4:]).decode()
            cmd = msg.split('\x1E')[0]
            to_send = ""
            if cmd=="ROMS":
                to_send = "RMDT\x1E"
                for i in self.rooms:
                    to_send += str(i)+"|"
                to_send = secure.encrypt(to_send.encode())
                self.socket.sendto(to_send, addr)
            if cmd=="JOIN":
                room_id = msg.split('\x1E')[1]
                for i in self.rooms:
                    if i.room_id==int(room_id):
                        if len(i.players)<4:
                            player.room = i
                            i.players.append(player)
                            to_send = f"JOND\x1E{i.room_id}"
                to_send = secure.encrypt(to_send.encode())
                self.socket.sendto(to_send,addr)
                if to_send !="":
                    br = f"PLCN\x1E{player.room.room_id}\x1E{len(player.room.players)}"
                    player.room.broadcast(self.socket, br)
            if cmd=="LEAV":
                room = None
                if player.room != None:
                    room = player.room
                    player.room.remove_player(player)
                    player.room = None
                to_send = f"LEFT\x1E"
                to_send = secure.encrypt(to_send.encode())
                self.socket.sendto(to_send,addr)
                if room != None:
                    br = f"PLCN\x1E{room.room_id}\x1E{len(room.players)}"
                    room.broadcast(self.socket, br)
            if cmd == "REDY":
                state = msg.split('\x1E')[1]
                player.ready = (state == "1")

                room = player.room
                if room:
                    ready_count = room.get_ready_count()

                    msg = f"RDYC\x1E{room.room_id}\x1E{ready_count}"
                    room.broadcast(self.socket, msg)
    def find_player(self,addr):
        for player in self.players:
            if player.addr == addr:
                return player
        return None
    def start_rooms(self):
        for i in range(1, 6):
            self.rooms.append(Room(i))

    def add_room(self):
        if len(self.rooms)<30:
            self.rooms.append(Room(len(self.rooms)+1))

    def print_rooms(self):
        for i in self.rooms:
            print(i)

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.max_players = MAX_PLAYERS
        self.players = []
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
        for player in self.players:
            sec = SecureSession(player.aes_key)
            encrypted = sec.encrypt(msg.encode())
            socket.sendto(encrypted, player.addr)
    def get_ready_count(self):
        count = 0
        for p in self.players:
            if p.ready == True:
                count+=1
        return count

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

    def remove_player(self, player):
        for i in self.players:
            if i==player:
                self.players.remove(player)

    def __str__(self):
        return f"Id: {self.room_id}\nStarted: {self.started}\nPlayerCount: {len(self.players)}"