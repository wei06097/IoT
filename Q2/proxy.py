import socket, random, time, os
from dotenv import load_dotenv

load_dotenv()
proxy_host = os.getenv("proxy_delay_host")
proxy_port = int(os.getenv("proxy_delay_port"))
client_host = os.getenv("client_host")
client_port = int(os.getenv("client_port"))

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.bind((proxy_host, proxy_port))
print("UDP Proxy Ready")

while True:
    recv_data, server_address = c.recvfrom(65535)
    tr = time.time()
    c.sendto(recv_data, (client_host, client_port))

    message_from_send = recv_data.decode("utf-8")
    message, ts, t0 = message_from_send.split('/')
    # print(f"[{message}] UDP Proxy received")
    print(f"[{message}] UDP Proxy received at t={float(tr)-float(t0):.3f} (delay={float(tr)-float(ts):.3f})")
    