import socket
import time

host = "127.0.0.1"
# port = 5406 # loss
port = 5408 # delay

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(1, 101):
    message = f"Packet {format(i,"3d")} sended at t = {format(time.time(),".5f")}"
    print(message)

    s.sendto(message.encode("utf-8"), (host, port))
    time.sleep(0.1)
