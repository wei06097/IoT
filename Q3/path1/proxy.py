import socket, random, time, os
from dotenv import load_dotenv

load_dotenv()
proxy_host = os.getenv("proxy_loss_host")
proxy_port = int(os.getenv("proxy_loss_port"))
client_host = os.getenv("client_host1")
client_port = int(os.getenv("client_port1"))

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.bind((proxy_host, proxy_port))
print("UDP Proxy with port 5406")

N = 10
i = 0
count = 0
while True:
    recv_data, server_address = c.recvfrom(65535)
    tr = time.time()
    message_from_send = recv_data.decode("utf-8")
    message, ts, t0 = message_from_send.split('/')

    pick = random.random()
    if pick <= 0.1:
        print(f"[{message}] *** Loss ***")
        count += 1
    else:
        c.sendto(recv_data, (client_host, client_port))
        # print(f"[{message}] UDP Proxy received")
        print(f"[{message}] UDP Proxy received at t={float(tr)-float(t0):.3f} (delay={float(tr)-float(ts):.3f})")
    
    i += 1
    if i == N:
        print(f"loss rate = {count/N*100}%")
        print(f"==============================")
        i = 0
        count = 0
    