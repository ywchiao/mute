#!python

import socket
import threading

def chatInput(connection):
    while True:
        text = input()
        connection.sendall(text.encode())

def chatMessage(connection):
    while True:
        data = connection.recv(1024)
        print(f"{data.decode()}")

        if data.decode() == "shutdown":
            break

def chatClient(HOST, PORT):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connection.connect((HOST, PORT))
    connection.sendall("Hello, world.".encode())

    threading.Thread(target=chatInput, args=(connection,)).start()
    threading.Thread(target=chatMessage, args=(connection,)).start()

if __name__ == "__main__":
    chatClient("127.0.0.1", 4004)
