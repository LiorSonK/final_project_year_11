import socket
class Server:
    def __init__(self,ip,port):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind((ip,port))
        self.shutdown = False
        self.players = 0
        self.threads = []
    def handle_client(self):
        pass
    def add_thread(self,thread):
        self.threads.append(thread)
    def join_threads(self):
        for t in self.threads:
            t.join()