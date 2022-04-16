chunk_size = 100

def read_file(path):
    res = ''
    for line in  open(path, "r", encoding='utf-8'):
        res += line
    return res

def make_pakets(data):
    bytes = data.encode()
    left = 0
    right = chunk_size
    res = []
    while(right <= len(bytes)):
        res.append(bytes[left:right])
        left = right
        right += chunk_size
    if left < len(bytes):
        res.append(bytes[left:])
    return res

def decode_packets(ps):
    return b''.join(ps).decode()

d = read_file('test_data.txt')


#print(  len("ACK".encode()))