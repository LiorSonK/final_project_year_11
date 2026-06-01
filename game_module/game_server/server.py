import threading
from server_constants import *
from server_class import Server
from login_module.login_server.loginServer import RunSrvr

def main ():
    global  all_to_die
    server = Server(IP,PORT)
    server.start_rooms()
    server.print_rooms()
    threading.Thread(target=RunSrvr, args=(server,), daemon=True).start()
    while True:
        data, addr = server.socket.recvfrom(1024)
        server.handle_msg(data,addr)
        if server.playerCount == 100:
            print("overload")
            break

    server.shutdown = True
    print('Main thread: waiting to all clints to die')
    server.join_threads()
    server.socket.close()
    print('Bye ..')

if __name__ == '__main__':
    main()