#!python

import socket
import threading

class Client():
    def __init__(self):
        pass

    def connect(self, HOST, PORT):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._socket.connect((HOST, PORT))

        threading.Thread(target=self._handler, args=()).start()

    def _user_input(self):
        while True:
            text = input()
            self._socket.sendall(text.encode())

    def _handler(self):
        while True:
            data = self._socket.recv(1024)

            msg_list = data.decode().split('\n')

            for msg in msg_list:
                if msg == "shutdown":
                    break
                elif msg == "user_id":
                    user_id = input("ID: ")
                    self._socket.sendall(f"user_id: {user_id}".encode())
                elif msg == "passwd":
                    passwd = input("密碼: ")
                    self._socket.sendall(f"passwd: {passwd}".encode())
                elif msg == "login_ok":
                    threading.Thread(target=self._user_input, args=()).start()
                else:
                    print(msg)

if __name__ == "__main__":
    client = Client()

    client.connect("127.0.0.1", 4004)
