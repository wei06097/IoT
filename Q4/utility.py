def split_string(string, batch):
    k, m = divmod(len(string), batch)
    return [string[i*k + min(i, m): (i+1)*k + min(i+1, m)] for i in range(batch)]

def get_dict_by_id(data, dict_id):
    return next((item for item in data if item.get("nth-package") == dict_id), None)

def get_part_size(nsize, batch, i):
    k, m = divmod(nsize, batch)
    return ((i+1)*k + min(i+1, m)) - (i*k + min(i, m))
