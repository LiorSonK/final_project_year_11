from game_constants import *
import random


class Player:
    def __init__(self, username,quarter):
        self.username = username
        if quarter==1:
            self.x = random.randint(BOARD_X_LEN/2,BOARD_X_LEN-1)
            self.y = random.randint(0, BOARD_Y_LEN-1)
        elif quarter==2:
            self.x = random.randint(0,BOARD_X_LEN/2)
            self.y = random.randint(0, BOARD_Y_LEN-1)
        elif quarter==3:
            self.x = random.randint(0,BOARD_X_LEN/2)
            self.y = random.randint(0, BOARD_Y_LEN-1)
        elif quarter==4:
            self.x = random.randint(BOARD_X_LEN/2,BOARD_X_LEN-1)
            self.y = random.randint(BOARD_X_LEN/2, BOARD_Y_LEN-1)
        else:
            raise ValueError("quarter must be between 1 and 4")