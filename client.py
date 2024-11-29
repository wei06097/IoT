import socket, time, os
from dotenv import load_dotenv

load_dotenv()
client_host = os.getenv("client_host")
client_port = int(os.getenv("client_port"))

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.bind((client_host, client_port))

time_out_time = 10
c.settimeout(time_out_time)

while True:
    try:
        recv_data, server_address = c.recvfrom(65535)
        recv_time = time.time()

        message_from_send = recv_data.decode("utf-8")
        temp = message_from_send.split()

        trans_time = float(temp[6])
        packet_delay = recv_time - trans_time

        print(f"message_from_send | Packet delay = {format(packet_delay,"1.5f")} sec")
        print(recv_data)
    
    except socket.timeout:
        print(f"*** Timeout while no input packet for {time_out_time} sec***")
        break
    