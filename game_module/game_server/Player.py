class Player:
    def __init__(self, username,addr,aes_key):
        self.username = username
        self.room = None
        self.addr = addr
        self.aes_key = aes_key