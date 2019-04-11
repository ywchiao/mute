
import selectors
import socket
import types

users = []

def reception(socket, multiplexer):
    connection, address = socket.accept()  # Should be ready to read
    print(f"Connected by: {address}")

    connection.setblocking(False)

    user = types.SimpleNamespace(
        address=address,
        id="anonymous",
        in_buffer=b'',
        out_buffer=b''
    )

    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    multiplexer.register(connection, events, data=user)

    users.append(user)

    user.out_buffer += (
        f"歡迎來到 MUTE: Multi-User Texting Environment\nuser_id".encode()
    )

def cmd_service(io, mask, multiplexer):
    connection = io.fileobj
    user = io.data

    if mask & selectors.EVENT_READ:
        user.in_buffer = connection.recv(1024)

        if user.in_buffer:
            cmd = user.in_buffer.decode().split(":")

            if cmd[0] == "user_id":
                user.id = cmd[1].strip()

                user.out_buffer += f"passwd".encode()
            elif cmd[0] == "passwd":
                user.out_buffer += f"login_ok\nMUTE 說: 登入成功!\n".encode()

                for usr in users:
                    usr.out_buffer += (
                        f"MUTE 說：使用者 {user.id} 進入 MUTE。".encode()
                    )
            else:
                message = (
                    f"{user.id} 說： ".encode() + user.in_buffer
                )

                for usr in users:
                    usr.out_buffer += message
        else:
            print(f"closing connection to {data.address}")
            multiplexer.unregister(connection)
            connection.close()

    if mask & selectors.EVENT_WRITE:
        if user.out_buffer:
            print(f"client {user.address}: {user.out_buffer.decode()}")

            sent = connection.send(user.out_buffer)
            user.out_buffer = user.out_buffer[sent:]

    return user.in_buffer.decode()

def serverlet(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind((HOST, PORT))
        serverSocket.setblocking(False)
        serverSocket.listen()

        multiplexer = selectors.DefaultSelector()
        multiplexer.register(serverSocket, selectors.EVENT_READ, data=None)

        print(f"MUTE server start listening at {HOST}:{PORT}")

        while True:
            events = multiplexer.select(timeout=None)

            for io, mask in events:
                if io.data is None:
                    reception(io.fileobj, multiplexer)
                else:
                    cmd = cmd_service(io, mask, multiplexer).split(":")

                    if cmd[0] == "shutdown":
                        exit()

if __name__ == "__main__":
    serverlet("127.0.0.1", 4004)
