import math
from reedsolo import RSCodec

def split_string(string, batch):
    k, m = divmod(len(string), batch)
    return [string[i*k + min(i, m): (i+1)*k + min(i+1, m)] for i in range(batch)]

def get_dict_by_id(data, dict_id):
    return next((item for item in data if item.get("nth-package") == dict_id), None)

def get_part_size(nsize, batch, i):
    k, m = divmod(nsize, batch)
    return ((i+1)*k + min(i+1, m)) - (i*k + min(i, m))

if __name__ == '__main__':
    n = 20
    batch = 20
    
    E = 0.3
    k = (17 + 1 + int(math.log10(n))) * batch
    nsize = math.ceil(k / (1 - 2*E))
    nsym = nsize - k
    rs = RSCodec(nsym=nsym, nsize=nsize)
    print('RS Ready')
    # for i in range(batch):
    #     print(get_part_size(nsize, batch, i))

    data = []
    origin_data = b""
    for i in range(1, batch+1):
        d = {
            "nth-package": i,
            "data": f"Data in package {i:0{int(math.log10(n)) + 1}}\n"
        }
        data.append(d)
        origin_data += d['data'].encode('utf-8')
    print(f"data:{len(origin_data)}, k:{k}, n:{nsize}, t:{(nsize-k)/2}, loss:{math.ceil(nsize*E)}\n")
    
    # RS Encode
    rs_data = rs.encode(origin_data)
    rs_arr = split_string(rs_data, batch)
    for i in range(len(data)):
        data[i]['data'] = list(rs_arr[i])
    
    # RS Decode
    rs_data = []
    for i in range(batch):
        d = get_dict_by_id(data, i+1)
        if i in [0]:
            for _ in range(get_part_size(nsize, batch, i)):
                rs_data += b" "
        elif not d == None:
            rs_data += d['data']
        else:
            for _ in range(get_part_size(nsize, batch, i)):
                rs_data += b" "
    
    res = rs.decode(rs_data)
    origin_data = ''.join(chr(i) for i in res[0])
    print(origin_data)
    