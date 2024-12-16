import json, math, time, socket, os, threading
from dotenv import load_dotenv
from reedsolo import RSCodec
from utility import split_string

load_dotenv()
E = float(os.getenv("E"))
N = int(os.getenv("N"))
batch = int(os.getenv("batch"))
interval = float(os.getenv("interval"))
server_host = os.getenv("server_host")
server_port = int(os.getenv("server_port"))
proxy_host = os.getenv("proxy_loss_host")
proxy_port = int(os.getenv("proxy_loss_port"))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((server_host, server_port))

lock = threading.Lock()
signal = -1
def listen_for_packets():
    global signal
    while True:
        data, addr = s.recvfrom(65535)
        count = int(data.decode("utf-8"))
        with lock:
            signal = count
        if count == N:
            break
        
if __name__ == '__main__':
    thread = threading.Thread(target=listen_for_packets)
    thread.start()

    ### RS Setting
    k = (17 + 1 + int(math.log10(N))) * batch
    nsize = math.ceil(k / (1 - 2*E))
    nsym = nsize - k
    rs = RSCodec(nsym=nsym, nsize=nsize)
    print('Server Ready')
    
    for batch_i in range(int(N / batch)):
        
        ### Original Packet Data
        data = []
        origin_data = b""
        for i in range(1, batch+1):
            nth = batch_i * batch + i
            d = {
                "nth-package": nth,
                "data": f"Data in package {nth:0{int(math.log10(N)) + 1}}\n"
            }
            data.append(d)
            origin_data += d['data'].encode('utf-8')
        
        ### RS Packet Data
        rs_data = rs.encode(origin_data)
        rs_arr = split_string(rs_data, batch)
        for i in range(len(data)):
            data[i]['data'] = list(rs_arr[i])
        
        # Send
        for packet in data:
            nth = packet["nth-package"]
            packet = json.dumps(packet)
            packet = packet.encode('utf-8')
            s.sendto(packet, (proxy_host, proxy_port))
            print(f"[Packet {nth:{int(math.log10(N))+1}d}] UDP Server sends")
            time.sleep(interval)
            with lock:
                if signal > nth:
                    signal = -1
                    break
    
    thread.join()
    packet = json.dumps({"nth-package": -1})
    packet = packet.encode('utf-8')
    s.sendto(packet, (proxy_host, proxy_port))
    