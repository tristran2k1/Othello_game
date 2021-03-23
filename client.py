import socket, re
import os
from init import ip
from bot import callBot
from bot import callBot_ai

HOST, PORT = ip(), 14003

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    while True:
        ret = str(sock.recv(1024), "ASCII")
        print(ret)
        if "winner" in ret:
            print("\nEND GAME!")
            callBot_ai(ret)
            break
        if re.match("victory_cell", ret) is None:
            break
        else:
            sock.sendall(bytes(callBot_ai(ret), "ASCII"))


