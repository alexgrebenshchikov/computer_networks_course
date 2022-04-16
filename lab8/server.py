import random
import socket
import file_io
import checksum

localIP = "127.0.0.1"

localPort = 20001

bufferSize = 1024


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

rec_data = []
prev_index = -1
end_packet_number = 255
packets = []

def write_uploaded_file(data, path):
    f = open(path, "w", encoding='utf-8')
    f.write(file_io.decode_packets(data))
    f.close()


def prepare_packets(byteAddrPair):
    global packets
    try:
        decodedMsg = byteAddrPair[0][5:].decode()
        if decodedMsg.startswith("download:"):
            print(decodedMsg[9:])
            packets = file_io.make_pakets(file_io.read_file(decodedMsg[9:]))
    except:
        pass

def save_packet(byteAddrPair, p_index):
    global prev_index, rec_data
    if(p_index != prev_index):
        rec_data.append(byteAddrPair[0][5:])
        prev_index = p_index
        
    if(p_index == 255):
        write_uploaded_file(rec_data, "server_file.txt")
        rec_data = []

    


while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    if checksum.calc_checksum(bytesAddressPair[0]) != 0:
        print("Incorrect checksum.")
        continue
    
    packet_number = bytesAddressPair[0][2]
    packet_index = bytesAddressPair[0][3]
    is_need_to_send = bytesAddressPair[0][4] == 1
    
    if is_need_to_send and len(bytesAddressPair[0]) >= 3:
        prepare_packets(bytesAddressPair)
    
    
    if not is_need_to_send:
        save_packet(bytesAddressPair, packet_index)
       

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{} {} {}".format(packet_number, packet_index, is_need_to_send)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    bytesToSend = bytes([packet_number]) + ("ACK").encode()
    if is_need_to_send:
        index_to_send = packet_index if packet_index < len(packets) - 1 else end_packet_number
        bytesToSend += bytes([index_to_send]) + packets[packet_index]
    bytesToSend = checksum.add_checksum_to_packet(bytesToSend)
    
    if random.randint(0, 100) > 15:
        UDPServerSocket.sendto(bytesToSend, address)

