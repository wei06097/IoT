import json, math, random, time, socket, os
from dotenv import load_dotenv

load_dotenv()
N = int(os.getenv("N"))
proxy_host = os.getenv("proxy_loss_host")
proxy_port = int(os.getenv("proxy_loss_port"))
client_host = os.getenv("client_host")
client_port = int(os.getenv("client_port"))

if __name__ == '__main__':
    total = 0
    count = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((proxy_host, proxy_port))
    print('Proxy Ready')

    while True:
        recv_data, server_address = s.recvfrom(65535)
        message_from_send = recv_data.decode("utf-8")

        data = json.loads(message_from_send)
        nth = data["nth-package"]

        if not nth == -1:
            total += 1
            pick = random.random()
            if pick < 0.1:
                print(f"*** Packet {nth:{int(math.log10(N))+1}d} Loss ***")
                count += 1
            else:
                # print(f"[Packet {nth:{int(math.log10(N))+1}d}] UDP Proxy received")
                s.sendto(recv_data, (client_host, client_port))
        else:
            s.sendto(recv_data, (client_host, client_port))
            print(f"loss:{count}, total: {total}, rate:{round(count/total*100, 3)}%")
            break
        