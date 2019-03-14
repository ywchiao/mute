#!python

import socket

def echoClient(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.connect((HOST, PORT))
        connection.sendall("Hello, world.".encode())

        while True:
            data = connection.recv(1024)
            print(f"echoed: {data.decode()}")

            if data.decode() == "shutdown":
                break

            text = input("you said: ")
            connection.sendall(text.encode())

if __name__ == "__main__":
    echoClient("127.0.0.1", 4004)
