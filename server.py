import socket, time, os
from dotenv import load_dotenv

load_dotenv()
proxy_host = os.getenv("proxy_loss_host")
proxy_port = int(os.getenv("proxy_loss_port"))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
t0 = time.time()

for i in range(1, 101):
    message = f"Packet {i:3d} sended at sec = {time.time()-t0:.2f}"
    print(message)
    
    s.sendto(message.encode("utf-8"), (proxy_host, proxy_port))
    time.sleep(0.1)
    