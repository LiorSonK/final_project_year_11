import threading
from server_constants import *
from server_class import Server


def main ():
    global  all_to_die
    server = Server(IP,PORT)
    server.socket.listen(20)
    while True:
        print('\nMain thread: before accepting ...')
        cli_sock,addr = server.socket.accept()
        t = threading.Thread(target = server.handle_client, args=(cli_sock,addr))
        t.start()
        server.add_thread(t)
        if server.players == 100:
            print("overload")
            break

    server.shutdown = True
    print('Main thread: waiting to all clints to die')
    server.join_threads()
    server.socket.close()
    print('Bye ..')

if __name__ == '__main__':
    main()