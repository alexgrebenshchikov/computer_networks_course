from checksum import add_checksum_to_packet, calc_checksum

def test_correct_even():
    pc = add_checksum_to_packet(bytes([175,110,255,124,252, 12]))
    assert(calc_checksum(pc) == 0)

def test_correct_odd():
    pc = add_checksum_to_packet(bytes([122,110,255,124,198]))
    assert(calc_checksum(pc) == 0)

def test_incorrect():
    pc = add_checksum_to_packet(bytes([122,110,255,124,198]))
    corrupted_pc = b'\xc1\x13zn\xff|\xc6'
    assert(calc_checksum(corrupted_pc) != 0)


test_correct_even()
test_correct_odd()
test_incorrect()