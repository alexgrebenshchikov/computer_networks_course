import socket
from timeit import default_timer as timer

serverAddressPort = ("127.0.0.1", 20001)

bufferSize = 1024


UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


number = 1
rtt_min = None
rtt_max = None
rtt_mean = 0
for _ in range(10):
    bytesToSend = str.encode("Ping {} {}".format(number, timer()))
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    UDPClientSocket.settimeout(1.0)

    try:
        start = timer()
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        rtt = (timer() - start) * 1000
        rtt_min = rtt if rtt_min is None else min(rtt, rtt_min)
        rtt_max = rtt if rtt_max is None else max(rtt, rtt_max)
        rtt_mean = (rtt_mean * (number - 1) + rtt) / number

        msg = "Message from Server {}, MIN RTT: {} ms, MAX RTT: {} ms, MEAN RTT: {} ms".\
            format(msgFromServer[0].decode('windows-1251'), rtt_min, rtt_max, rtt_mean)
        print(msg)
        number += 1
    except TimeoutError:
        print("Request timed out")


print("Lost packets ratio: {}".format((10 - number + 1) / 10))



