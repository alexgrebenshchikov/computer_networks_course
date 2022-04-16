import socket
import file_io
from timeit import default_timer as timer

import random
import checksum

serverAddressPort = ("127.0.0.1", 20001)

bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def write_downloaded_file(data, path):
    f = open(path, "w", encoding='utf-8')
    f.write(file_io.decode_packets(data))
    f.close()


upload_flag = 0
download_flag = 1

def upload_file_to_server(path_to_file):
    packets = file_io.make_pakets(file_io.read_file(path_to_file))
    assert(len(packets) < 256)

    timeout = 1.0
    number = 0
    success_sends = 0
    end_packet_number = 255
    while(True):
        if success_sends == len(packets):
            break
        bytesToSend = bytes([number, success_sends if success_sends != len(packets) - 1 else end_packet_number, upload_flag]) + packets[success_sends]
        bytesToSend = checksum.add_checksum_to_packet(bytesToSend)
        if random.randint(0, 100) > 15:
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        
        spend_time = 0.0
        while(True):
            UDPClientSocket.settimeout(timeout - spend_time)

            try:
                start = timer()
                bFromServer = UDPClientSocket.recvfrom(bufferSize)[0]
                if checksum.calc_checksum(bFromServer) != 0:
                    print("Incorrect checksum.")
                    break
                
                msgFromServer = "{}{}".format(bFromServer[2], bFromServer[3:].decode())
                print(msgFromServer)
                if msgFromServer == "{}ACK".format(number):
                    number = (number + 1) % 2
                    success_sends += 1
                    break
                else:
                    print("NOT ACK")
                
                spend_time += (timer() - start)
                if spend_time > timeout:
                    print("Request timed out")
                    break
                
                
            except TimeoutError:
                print("Request timed out")
                break


def download_file_from_server(path_to_file):
    timeout = 1.0
    number = 0
    success_sends = 0
    end_packet_number = 255
    downloading_acquired = False
    rec_data = []
    while(True):
        
        bytesToSend = bytes([number, success_sends, download_flag]) if downloading_acquired else bytes([number, success_sends, download_flag]) + ("download:" + path_to_file).encode()
        bytesToSend = checksum.add_checksum_to_packet(bytesToSend)
        if random.randint(0, 100) > 15:
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        
        spend_time = 0.0
        while(True):
            UDPClientSocket.settimeout(timeout - spend_time)

            try:
                start = timer()
                bFromServer = UDPClientSocket.recvfrom(bufferSize)[0]
                if checksum.calc_checksum(bFromServer) != 0:
                    print("Incorrect checksum.")
                    break
                
                msgFromServer = "{}{}".format(bFromServer[2], bFromServer[3:6].decode())
                packet_index = bFromServer[6]
                print(msgFromServer, packet_index)
                if msgFromServer == "{}ACK".format(number):
                    number = (number + 1) % 2
                    success_sends += 1
                    downloading_acquired = True
                    rec_data.append(bFromServer[7:])
                    if packet_index == end_packet_number:
                        print('done')
                        write_downloaded_file(rec_data, "client_file.txt")
                        return
                    break
                else:
                    print("NOT ACK")
                
                spend_time += (timer() - start)
                if spend_time > timeout:
                    print("Request timed out")
                    break
                
                
            except TimeoutError:
                print("Request timed out")
                break



upload_file_to_server("test_data.txt")
download_file_from_server("test_data.txt")
