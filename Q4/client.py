import json, math, time, socket, os
from datetime import timedelta
from collections import deque
from reedsolo import RSCodec
from dotenv import load_dotenv
from utility import get_dict_by_id, get_part_size

filename = "log.txt"
load_dotenv()
E = float(os.getenv("E"))
N = int(os.getenv("N"))
batch = int(os.getenv("batch"))
client_host = os.getenv("client_host")
client_port = int(os.getenv("client_port"))
server_host = os.getenv("server_host")
server_port = int(os.getenv("server_port"))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((client_host, client_port))
with open(filename, "w") as file:
    file.write("")

if __name__ == "__main__":
    ### RS Setting
    k = (17 + 1 + int(math.log10(N))) * batch
    nsize = math.ceil(k / (1 - 2*E))
    nsym = nsize - k
    rs = RSCodec(nsym=nsym, nsize=nsize)
    print(f"k:{k}, n:{nsize}, t:{(nsize-k)/2}, loss:{math.ceil(nsize*E)}")
    print('Client Ready')
    
    t0 = 0
    tn = 0
    count = 0
    rs_data = []
    buffer = deque()
    while True:
        
        ### Receive Data
        recv_data, server_address = s.recvfrom(65535)
        recv_data = recv_data.decode("utf-8")
        recv_data = json.loads(recv_data)
        buffer.append(recv_data)
        nth = recv_data['nth-package']
        if t0 == 0:
            t0 = time.time()
        tn = time.time()
        print(f"[Packet {nth:{int(math.log10(N))+1}d}] UDP Client received")
        
        signal = len(buffer) >= (1-E)*batch
        # if len(buffer) == batch or (signal and N-count == batch):
        if len(buffer) == batch or signal:
            if signal:
                s.sendto(f'{count+batch}'.encode('utf-8'), (server_host, server_port))
            
            for i in range(batch):
                if not len(buffer) == 0:
                    packet = buffer.popleft()
                    nth = packet['nth-package']
                count += 1
                if count == nth:
                    rs_data += packet['data']
                else:
                    buffer.appendleft(packet)
                    for _ in range(get_part_size(nsize, batch, i)):
                        rs_data += b" "
            
            while not len(buffer) == 0:
                packet = buffer.popleft()
                nth = packet['nth-package']
                if nth > count:
                    buffer.appendleft(packet)
                    break
            
            res = rs.decode(rs_data)
            origin_data = ''.join(chr(i) for i in res[0])
            rs_data = []
        
            ### Write File
            with open(filename, "a") as file:
                origin_data = origin_data.replace("\n", f"\t{tn}\n")
                file.write(origin_data)
        
        if count == N:
            td = str(timedelta(seconds=tn-t0)).split('.')[0]
            print(f"total time: {td}")
            break
        