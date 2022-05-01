import struct
from Checksum import *
from IcmpDataStruct import *


def split_bytes(bts, split_index):
    return bts[:split_index], bts[split_index:]


class ICMP:
    REQUEST_TYPE = 8
    REQUEST_CODE = 0

    HEADER_LEN = 4
    STRUCT_FORMAT = 'BBH'
    IP_HEADER_LEN = 20

    def __init__(self, typ, code, checksum, data):
        self._type = typ
        self._code = code
        self._checksum = checksum
        self._data = data

    @staticmethod
    def build_header(typ, code, checksum):
        return struct.pack(ICMP.STRUCT_FORMAT, typ, code, checksum)

    @staticmethod
    def create(typ, code, data):
        header_without_checksum = ICMP.build_header(typ, code, 0)
        checksum = calc_checksum(header_without_checksum + data.to_bytes())
        return ICMP(typ, code, checksum, data)

    @staticmethod
    def create_request(ids, seq, time_ms):
        echo_data = EchoData.create(ids, seq, time_ms)
        return ICMP.create(ICMP.REQUEST_TYPE, ICMP.REQUEST_CODE, echo_data)

    @staticmethod
    def parse_header(header):
        return struct.unpack(ICMP.STRUCT_FORMAT, header)

    @staticmethod
    def parse_data(typ, data):
        if typ == 0 or typ == 8:
            return EchoData.from_bytes(data)
        if typ == 3:
            return ErrorData.from_bytes(data)
        return None

    @staticmethod
    def parse_packet(ip_packet):
        _, icmp_part = split_bytes(ip_packet, ICMP.IP_HEADER_LEN)
        if not checksum_check(icmp_part):
            print('Wrong checksum!')
            return None
        header_bytes, data_bytes = split_bytes(icmp_part, ICMP.HEADER_LEN)
        typ, code, checksum = ICMP.parse_header(header_bytes)
        data = ICMP.parse_data(typ, data_bytes)
        return ICMP(typ, code, checksum, data)

    def to_bytes(self):
        header = self.build_header(self._type, self._code, self._checksum)
        return header + self._data.to_bytes()





