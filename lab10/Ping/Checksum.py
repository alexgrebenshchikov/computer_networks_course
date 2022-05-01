from more_itertools import chunked


BLOCK_SIZE = 2
BASE = BLOCK_SIZE * 8
MAX_VALUE = (1 << BASE) - 1

def calc_checksum(data: bytes) -> int:
    res = 0
    
    for block in chunked(data, BLOCK_SIZE):      
        res += int.from_bytes(block, 'little')
    
    while res & MAX_VALUE != res:
        res = (res >> BASE) + (res & MAX_VALUE)
    return MAX_VALUE ^ res

def checksum_check(data: bytes) -> bool:
    return calc_checksum(data) == 0