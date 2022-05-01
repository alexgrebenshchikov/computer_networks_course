import struct

from IcmpStruct import *


def split_bytes(bts, split_index):
    return bts[:split_index], bts[split_index:]

class ICMPData:

    @staticmethod
    def from_bytes(raw_data):
        pass

    def to_bytes(self):
        pass


class ErrorData(ICMPData):
    HEADER_LEN = 4
    STRUCT_FORMAT = 'HH'

    def __init__(self, icmp, unused=None):
        self.icmp = icmp
        if unused is None:
            unused = struct.pack(ErrorData.STRUCT_FORMAT, 0, 0)
        self.unused = unused

    def to_bytes(self):
        return self.unused + self.icmp.to_bytes()

    @staticmethod
    def from_bytes(raw_data):
        unused, nested_ip_packet = split_bytes(raw_data, ErrorData.HEADER_LEN)
        nested_icmp = ICMP.parse_packet(nested_ip_packet)
        return ErrorData(nested_icmp, unused)


class EchoData(ICMPData):
    HEADER_LEN = 4
    STRUCT_FORMAT = 'HH'

    def __init__(self, ids, seq, data):
        self._id = ids
        self._seq = seq
        self._data = data

    def to_bytes(self):
        header = struct.pack(EchoData.STRUCT_FORMAT, self._id, self._seq)
        return header + self._data

    @staticmethod
    def create(ids, seq, time_ms):
        data = time_ms.to_bytes(8, byteorder='big')
        return EchoData(ids, seq, data)

    @staticmethod
    def from_bytes(raw_data):
        header, data = split_bytes(raw_data, EchoData.HEADER_LEN)
        ids, seq = struct.unpack(EchoData.STRUCT_FORMAT, header)
        return EchoData(ids, seq, data)
