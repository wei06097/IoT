import socket
import random
import time
import threading

proxy_ip = "127.0.0.1"
proxy_port = 5408
host = "127.0.0.1"
port = 5405 #5407

count = 0
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.bind((proxy_ip, proxy_port))

def delay_func(recv_data, flag):
    time.sleep(0.5)
    c.sendto(recv_data, (host, port))
    print(f"*** Packet {format(flag,'3d')} Released ***")

N = 100
while True:
    try:
        recv_data, server_address = c.recvfrom(65535)
        message_from_send = recv_data.decode("utf-8")

        temp = message_from_send.split()
        flag = int(temp[1])

        pick = random.random()
        if pick <= 0.05:
            print(f"*** Packet {format(flag,'3d')} Delayed ***")
            thread_ = threading.Thread(target=delay_func, args=(recv_data, flag))
            thread_.start()
            count += 1
        else:
            c.sendto(recv_data, (host, port))
        
        if flag == N:
            print(f"delay rate = {count/N*100}%")
            break
    
    except socket.timeout:
        print(f"*** Timeout while no input packet for {time_out_time} sec***")
        break
    