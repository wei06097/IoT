import socket, time, os
from dotenv import load_dotenv

load_dotenv()
proxy_host = os.getenv("proxy_loss_host")
proxy_port = int(os.getenv("proxy_loss_port"))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
t0 = time.time()
print("UDP Server")

for i in range(1, 11):
    message = f"Packet {i:2d}/{time.time()}/{t0}"
    s.sendto(message.encode("utf-8"), (proxy_host, proxy_port))

    message, ts, t0 = message.split('/')
    print(f"[{message}] UDP Server sends at t={float(ts)-float(t0):.3f}")
    
    time.sleep(0.1)
    