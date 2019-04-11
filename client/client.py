#!python

import socket
import threading

def user_input(connection):
    while True:
        text = input()
        connection.sendall(text.encode())

def cmd_handler(connection):
    while True:
        data = connection.recv(1024)

        msg_list = data.decode().split('\n')

        for msg in msg_list:
            if msg == "shutdown":
                break
            elif msg == "user_id":
                user_id = input("ID: ")
                connection.sendall(f"user_id: {user_id}".encode())
            elif msg == "passwd":
                passwd = input("密碼: ")
                connection.sendall(f"passwd: {passwd}".encode())
            elif msg == "login_ok":
                threading.Thread(target=user_input, args=(connection,)).start()
            else:
                print(msg)

def client(HOST, PORT):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connection.connect((HOST, PORT))

    threading.Thread(target=cmd_handler, args=(connection,)).start()

if __name__ == "__main__":
    client("127.0.0.1", 4004)
