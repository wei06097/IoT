import socket
import random
import time

proxy_ip = "127.0.0.1"
proxy_port = 5406
host = "127.0.0.1"
port = 5405

count = 0
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.bind((proxy_ip, proxy_port))

N = 100
while True:
    try:
        recv_data, server_address = c.recvfrom(65535)
        message_from_send = recv_data.decode("utf-8")

        temp = message_from_send.split()
        flag = int(temp[1])

        pick = random.random()
        if pick <= 0.1:
            print(f"*** Packet {format(flag,'3d')} Loss ***")
            count += 1
        else:
            c.sendto(recv_data, (host, port))
        
        if flag == N:
            print(f"loss rate = {count/N*100}%")
            break
    
    except socket.timeout:
        print(f"*** Timeout while no input packet for {time_out_time} sec***")
        break
    