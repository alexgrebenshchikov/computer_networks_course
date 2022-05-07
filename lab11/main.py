import time
import socket
from node import Node
from threading import Thread
from nodeinfo import NodeInfo
from node import REQUEST_TYPE_WEIGHT, REQUEST_TYPE_STOP


def set_new_weight(sckt, a, b, new_weight):
    sckt.sendto(f'{REQUEST_TYPE_WEIGHT}::{a.name}::{new_weight}'.encode(), (b.host, b.port))
    sckt.sendto(f'{REQUEST_TYPE_WEIGHT}::{b.name}::{new_weight}'.encode(), (a.host, a.port))


if __name__ == '__main__':
    HOST = '127.0.0.1'

    node_info_0 = NodeInfo('0', HOST, 80)
    node_info_1 = NodeInfo('1', HOST, 81)
    node_info_2 = NodeInfo('2', HOST, 82)
    node_info_3 = NodeInfo('3', HOST, 83)

    node_0 = Node(node_info_0, [node_info_1, node_info_2, node_info_3], {'1': 1, '2': 3, '3': 7})
    node_1 = Node(node_info_1, [node_info_0, node_info_2], {'0': 1, '2': 1})
    node_2 = Node(node_info_2, [node_info_0, node_info_1, node_info_3], {'0': 3, '1': 1, '3': 2})
    node_3 = Node(node_info_3, [node_info_0, node_info_2], {'0': 7, '2': 2})

    nodes = [node_0, node_1, node_2, node_3]

    for node in nodes:
        Thread(target=node.listen_for_requests).start()

    time.sleep(5)

    main_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print('Changing weights...\n')
    set_new_weight(main_socket, node_info_0, node_info_3, 3)
    set_new_weight(main_socket, node_info_1, node_info_2, 5)
    set_new_weight(main_socket, node_info_0, node_info_2, 8)

    time.sleep(20)

    for node in nodes:
        main_socket.sendto(f'{REQUEST_TYPE_STOP}::::'.encode(), (node.info.host, node.info.port))
