import argparse
from time import sleep
from PingClient import PingClient
from Statistics import Statistics
from PingResponse import PingResponse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs='?', const=1, type=str)
    parser.add_argument('--packet_number', nargs='?', const=1, default=12, type=int)
    parser.add_argument('--timeout', nargs='?', const=1, default=1000, type=int)
    parser.add_argument('--ttl', nargs='?', const=1, default=231, type=int)
    args = parser.parse_args()
    return args.host, args.packet_number, args.timeout, args.ttl


if __name__ == '__main__':
    stats = Statistics()
    host, request_count, timeout_ms, ttl = parse_args()
    ping_client = PingClient(timeout_ms, ttl)

    address = None
    for request_index in range(request_count):
        address, packet_len, ping_response, rtt_ms = ping_client.ping(host, seq=request_index + 1)

        if ping_response == PingResponse.SUCCESS:
            print(f'Ответ от {address}: число байт={packet_len} время={rtt_ms}мс TTL={ttl}')
            stats.register_rtt(rtt_ms)
        else:
            print(f'Unexpected error: {ping_response.name}')
            stats.register_missed()

        if rtt_ms < timeout_ms:
            sleep((timeout_ms - rtt_ms) / 1000)

    if address is not None:
        stats.print_statistics(address)
