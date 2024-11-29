import socket, random, os
from dotenv import load_dotenv

load_dotenv()
proxy_host = os.getenv("proxy_loss_host")
proxy_port = int(os.getenv("proxy_loss_port"))
client_host = os.getenv("client_host")
client_port = int(os.getenv("client_port"))

count = 0
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.bind((proxy_host, proxy_port))

N = 100
while True:
    try:
        recv_data, server_address = c.recvfrom(65535)
        message_from_send = recv_data.decode("utf-8")

        temp = message_from_send.split()
        flag = int(temp[1])

        pick = random.random()
        if pick <= 0.1:
            print(f"*** Packet {flag:3d} Loss ***")
            count += 1
        else:
            c.sendto(recv_data, (client_host, client_port))
        
        if flag == N:
            print(f"loss rate = {count/N*100}%")
            break
    
    except socket.timeout:
        print(f"*** Timeout while no input packet for {time_out_time} sec***")
        break
    