
import selectors
import socket
import types

users = []

def echo_reception(socket, multiplexer):
    connection, address = socket.accept()  # Should be ready to read
    print(f"Connected by: {address}")

    connection.setblocking(False)

    data = types.SimpleNamespace(address=address, in_buffer=b'', out_buffer=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    multiplexer.register(connection, events, data=data)
    users.append(data)

def echo_service(io, mask, multiplexer):
    connection = io.fileobj
    data = io.data

    if mask & selectors.EVENT_READ:
        data.in_buffer = connection.recv(1024)

        if data.in_buffer:
            message = f"{str(data.address[1])} said: ".encode() + data.in_buffer

            for usr in users:
                usr.out_buffer += message
        else:
            print(f"closing connection to {data.address}")
            multiplexer.unregister(connection)
            connection.close()

    if mask & selectors.EVENT_WRITE:
        if data.out_buffer:
            print(f"client {data.address} said: {data.out_buffer.decode()}")

            sent = connection.send(data.out_buffer)
            data.out_buffer = data.out_buffer[sent:]

    return data.in_buffer.decode()

def echo_server(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind((HOST, PORT))
        serverSocket.setblocking(False)
        serverSocket.listen()

        multiplexer = selectors.DefaultSelector()
        multiplexer.register(serverSocket, selectors.EVENT_READ, data=None)

        print(f"Echo server start listening at {HOST}:{PORT}")

        while True:
            events = multiplexer.select(timeout=None)

            for io, mask in events:
                if io.data is None:
                    echo_reception(io.fileobj, multiplexer)
                else:
                    cmd = echo_service(io, mask, multiplexer)

                    if cmd == "shutdown":
                        exit()

if __name__ == "__main__":
    echo_server("127.0.0.1", 4004)
