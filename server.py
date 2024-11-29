import socket, time, os
from dotenv import load_dotenv

load_dotenv()
proxy_host = os.getenv("proxy_loss_host")
proxy_port = int(os.getenv("proxy_loss_port"))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(1, 101):
    message = f"Packet {format(i,"3d")} sended at t = {format(time.time(),".5f")}"
    print(message)

    s.sendto(message.encode("utf-8"), (proxy_host, proxy_port))
    time.sleep(0.1)
    