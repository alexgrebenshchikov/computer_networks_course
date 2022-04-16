def calc_checksum(bts):
    assert(len(bts) > 0)
    
    if len(bts) % 2 == 1:
        bts = bytes([0]) + bts

    return 0xFFFF - (sum([int.from_bytes(bts[i : i + 2], byteorder="big") for i in range(0, len(bts), 2)]) % 0x10000)

def add_checksum_to_packet(bts):
    ch_sum = int.to_bytes(calc_checksum(bts), length=2, byteorder="big")
    if len(bts) % 2 == 1:
        ch_sum = ch_sum[::-1]
    return ch_sum + bts






