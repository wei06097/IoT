import socket, time, os
from dotenv import load_dotenv

load_dotenv()
client_host = os.getenv("client_host2")
client_port = int(os.getenv("client_port2"))

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.bind((client_host, client_port))
print("UDP Client with port 5407")

while True:
    recv_data, server_address = c.recvfrom(65535)
    tr = time.time()

    message_from_send = recv_data.decode("utf-8")
    message, ts, t0 = message_from_send.split('/')
    print(f"[{message}] UDP Proxy received at t={float(tr)-float(t0):.3f} (delay={float(tr)-float(ts):.3f})")
    