import os
import socket
from PingResponse import PingResponse
from IcmpStruct import ICMP
from IcmpDataStruct import EchoData, ErrorData
from time import time
from random import randint




class PingClient:

    def __init__(self, timeout_ms, ttl):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        self.socket.settimeout(timeout_ms / 1000)

    def __del__(self):
        self.socket.close()

    def ping(self, host, port=1, seq = 0):
        try:
            host = socket.gethostbyname(host)
        except socket.gaierror:
            return host, -1, PingResponse.UNKNOWN_HOST, 0

        packet_id = randint(0, 0x10000)
        start_time = time()
        echo_packet = ICMP.create_request(packet_id, seq, int(start_time * 1000))
        self.socket.sendto(echo_packet.to_bytes(), (host, port))

        return host, len(echo_packet.to_bytes()), self.receive(packet_id,
                                                               seq), int((time() - start_time) * 1000)

    def receive(self, expected_id, expected_seq):
        try:
            while True:
                ip_packet, _ = self.socket.recvfrom(1024)
                icmp_reply = ICMP.parse_packet(ip_packet)

                if isinstance(icmp_reply._data, EchoData):
                    echo_reply = icmp_reply._data
                    if echo_reply._id == expected_id and echo_reply._seq == expected_seq:
                        return PingResponse.SUCCESS

                if isinstance(icmp_reply._data, ErrorData):
                    error_reply = icmp_reply._data
                    nested = error_reply.icmp._data
                    if nested._id == expected_id and nested._seq == expected_seq:
                        return PingResponse.from_error_code(icmp_reply._code)

        except socket.timeout:
            return PingResponse.TIMEOUT
