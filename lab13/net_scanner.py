from ipaddress import ip_address
import socket
import PySimpleGUI as py_gui
import scapy.all as scapy

HOME_IP_ADDR = '192.168.0.196'
NETWORK_IP_ADDR = '192.168.0.1'
HOME_MAC_ADDR = '4C-D5-77-0D-0D-83'
HOME_HOST_NAME = socket.gethostbyaddr(HOME_IP_ADDR)[0]
MASK = [255, 255, 255, 0]

def scan_network(ip):
    return [
        {
            'ip': i[1].psrc,
            'mac': i[1].hwsrc
        }
        for i in scapy.srp(
            scapy.Ether(dst='ff:ff:ff:ff:ff:ff') / scapy.ARP(pdst=ip),
            timeout = 1,
            verbose = False)[0]    
    ]


def apply_mask(ip_addr):
    return [a & b for a, b in zip(MASK, list(map(lambda s: int(s), ip_addr.split('.'))))]

def check_ip_using_mask(ip_addr):
    return apply_mask(ip_addr) == apply_mask(HOME_IP_ADDR) 

clients = scan_network(f'{NETWORK_IP_ADDR}/24')
clients = list(filter(lambda host: host['ip'] != HOME_IP_ADDR and check_ip_using_mask(host['ip']), clients))

layout = [
    [py_gui.ProgressBar(len(clients) + 1, orientation='h', size=(50, 20), key='progress_bar')],
    [py_gui.Output(size=(100, 20), font=('Consolas', 10), key='out')],
    [py_gui.Submit('Start')]
]
window = py_gui.Window('Net scanner', layout)

while True:
    event, values = window.read(timeout=100)

    if event in (None, 'Exit'):
        break

    if event == 'Start':
        window.FindElement('out').Update('')

        print(f'{"IP address":30}{"MAC address":30}{"Host name":30}')
        print('My computer:')
        print(f'{HOME_IP_ADDR:30}{HOME_MAC_ADDR:30}{HOME_HOST_NAME:30}')
        print('Network:')

        progress_bar = window['progress_bar']
        progress_bar.UpdateBar(1)
        for i, host in enumerate(clients):
            ip_addr, mac_address = host['ip'], host['mac']
            
            try:
                host_name = socket.gethostbyaddr(ip_addr)[0]
            except Exception:
                host_name = 'Not found'
            print(f'{str(ip_addr):30}{str(mac_address):30}{str(host_name):30}')
            progress_bar.UpdateBar(i + 2)

window.close()