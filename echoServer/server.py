#!python

import socket

def echoServer(HOST, PORT):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind((HOST, PORT))
        serverSocket.listen()

        print(f"Echo server start listening at {HOST}:{PORT}")

        while True:
            connection, address = serverSocket.accept()

            with connection:
                print(f"Connected by: {address}")

                while True:
                    data = connection.recv(1024)
                    print(f"client said: {data.decode()}")

                    connection.sendall(data)

                    if data == "shutdown".encode():
                        exit()

if __name__ == "__main__":
    echoServer("127.0.0.1", 4004)
