import socket, random, time, threading, os
from dotenv import load_dotenv

load_dotenv()
proxy_host = os.getenv("proxy_delay_host")
proxy_port = int(os.getenv("proxy_delay_port"))
client_host = os.getenv("client_host")
client_port = int(os.getenv("client_port"))

count = 0
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.bind((proxy_host, proxy_port))

def delay_func(recv_data, flag):
    time.sleep(0.5)
    c.sendto(recv_data, (client_host, client_port))
    print(f"*** Packet {flag:3d} Released ***")

N = 100
while True:
    recv_data, server_address = c.recvfrom(65535)
    message_from_send = recv_data.decode("utf-8")

    temp = message_from_send.split()
    flag = int(temp[1])

    pick = random.random()
    if pick <= 0.05:
        print(f"*** Packet {flag:3d} Delayed ***")
        thread_ = threading.Thread(target=delay_func, args=(recv_data, flag))
        thread_.start()
        count += 1
    else:
        c.sendto(recv_data, (client_host, client_port))
    
    if flag == N:
        print(f"delay rate = {count/N*100}%")
        break
