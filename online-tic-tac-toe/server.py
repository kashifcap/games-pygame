import socket
from _thread import start_new_thread
import pickle


def threaded(conn, player):
    conn.send(str.encode(player))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                break
            else:
                if data[0] != -1:
                    row = data[0]
                    col = data[1]
                    if player == 'x':
                        board[row][col] = 'x'
                    elif player == 'o':
                        board[row][col] = 'o'
                
            conn.send(pickle.dumps(board))
        except:
            print("Disconnected")
            break
    conn.close()


def main():
    global board
    board = [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ip and port of server
    server = ""
    port = 5555

    player = 'x'

    s.bind((server, port))
    s.listen(2)
    print("Server is ready...")

    while True:
        conn, addr = s.accept()
        print("Connetcted to : ", addr)
        start_new_thread(threaded, (conn, player))
        player = 'o'


main()