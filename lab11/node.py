import ast
import copy
import socket
from distancelist import DistanceList
from nodeinfo import NodeInfo

REQUEST_TYPE_DIST_LIST = "dlist"
REQUEST_TYPE_WEIGHT = "weight"
REQUEST_TYPE_STOP = "stop"


class Node:
    def __init__(self, info: NodeInfo, neighbours, weights):
        self.receive_socket = None
        self.send_socket = None
        self.is_running = False
        self.info = copy.deepcopy(info)
        self.neighbours = copy.deepcopy(neighbours)
        self.weights = copy.deepcopy(weights)

        self.info.dist_list[self.info.name] = 0
        self.info.changed_dists[self.info.name] = self.info.name
        for neighbor in self.neighbours:
            self.info.dist_list[neighbor.name] = self.weights[neighbor.name]

        print(f'{self.info.name}: initial dist list: {self.info.dist_list}')

        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.send_socket.settimeout(0.1)

        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket.settimeout(0.1)
        self.receive_socket.bind((self.info.host, self.info.port))

        self.notify_neighbours()

    def receive(self):
        try:
            request, _ = self.receive_socket.recvfrom(1024)
            return request.decode()
        except socket.timeout:
            pass

    def send(self, message, to_node):
        self.send_socket.sendto(message.encode(), (to_node.host, to_node.port))

    def handle_request(self, request):
        typ, name, data = request.split('::')
        if typ == REQUEST_TYPE_DIST_LIST:
            dlist = ast.literal_eval(data)
            self.update_dist_list(name, dlist)
        if typ == REQUEST_TYPE_WEIGHT:
            weight = int(data)
            self.set_neighbour_weight(name, weight)
        if typ == REQUEST_TYPE_STOP:
            self.is_running = False

    def set_neighbour_weight(self, neighbor_name, new_weight):
        self.weights[neighbor_name] = new_weight
        self.info.dist_list[neighbor_name] = new_weight
        self.info.changed_dists[neighbor_name] = neighbor_name

    def update_dist_list(self, neighbor_name, neighbor_dv):
        for neighbor in self.neighbours:
            if neighbor.name == neighbor_name:
                neighbor.dist_list.update_dist_list(neighbor_dv)
                break

    def notify_neighbours(self):
        for to in self.neighbours:
            dist_list_final = copy.copy(self.info.dist_list.data)
            for remove_node_name in self.info.changed_dists:
                if self.info.changed_dists[remove_node_name] == to.name:
                    dist_list_final.pop(remove_node_name)

            message = f'{REQUEST_TYPE_DIST_LIST}::{self.info.name}::{dist_list_final}'
            self.send(message, to)

    def recalc_dist_list(self):
        new_dist_list = DistanceList()
        new_changed_dists = {}
        new_dist_list[self.info.name] = 0
        new_changed_dists[self.info.name] = self.info.name
        for neighbor in self.neighbours:
            w = self.weights[neighbor.name]
            for d in neighbor.dist_list.data:
                if new_dist_list.update_item(d, w + neighbor.dist_list[d]):
                    new_changed_dists[d] = neighbor.name

        if self.info.dist_list.data != new_dist_list.data:
            self.info.dist_list = new_dist_list
            self.info.changed_dists = new_changed_dists
            self.notify_neighbours()

    def listen_for_requests(self):
        self.is_running = True
        iteration_number = 1
        while self.is_running:
            request = self.receive()
            if request is not None:
                self.handle_request(request)
                self.recalc_dist_list()
            if iteration_number % 40 == 0:
                self.notify_neighbours()
            iteration_number += 1
        print(f'{self.info.name}: final dist list: {self.info.dist_list}')
