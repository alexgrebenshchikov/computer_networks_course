import datetime
from faulthandler import disable

import PySimpleGUI as gui

from util import *
from threading import Thread

RECEIVE_BUTTON_EVENT ='Получить пакеты'



host, port = DEFAULT_HOST, DEFAULT_PORT
tcp_socket = tcp_socket_init(host, port)
tcp_socket.listen(1)
udp_socket = udp_socket_init()
udp_socket.bind((host, port))

window = gui.Window('UDP получатель', [
    [gui.Text('Введите IP  адрес', size=DEFAULT_GUI_TEXT_SIZE), gui.InputText(host)],
    [gui.Text('Введите порт для получения', size=DEFAULT_GUI_TEXT_SIZE), gui.InputText(str(port))],
    [gui.Text('Скорость соединения', size=DEFAULT_GUI_TEXT_SIZE), gui.Text(key='speed')],
    [gui.Text('Число полученных пакетов', size=DEFAULT_GUI_TEXT_SIZE), gui.Text(key='count')],
    [gui.Button(RECEIVE_BUTTON_EVENT)],
])

total = 0
current = 0
left_ms = 0
right_ms = 0
speed = 0
is_packets_received = False

def receive_packets():
    global current, total, speed, is_packets_received
    current = 0
    left_ms = 0

    recv_tcp_socket = None
    try:
        recv_tcp_socket, _ = tcp_socket.accept()
        total = int(recv_tcp_socket.recv(PACKET_SIZE).decode())
    except Exception as e:
        print(e)
    finally:
        if recv_tcp_socket is not None:
            recv_tcp_socket.close()

    for _ in range(total):
        try:
            message, _ = udp_socket.recvfrom(PACKET_SIZE)
            message_time_ms, _ = message.decode().split()
            current += 1
            if left_ms == 0:
                left_ms = int(message_time_ms)
        except socket.timeout:
            pass
    right_ms = round(datetime.datetime.now().timestamp() * 1000)

    total_time_ms = right_ms - left_ms
    speed = 0
    if total_time_ms > 0:
        speed = round(PACKET_SIZE * current / total_time_ms)
    is_packets_received = True
 



while True:
    event, values = window.read(100)

    if event in (None, 'Exit'):
        break

    try:
        new_host, new_port = values[0], int(values[1])
    except Exception as e:
        print(e)
        continue

    if new_host != host or new_port != port:
        host, port = new_host, new_port
        udp_socket.close()
        tcp_socket.close()
        udp_socket = udp_socket_init()
        udp_socket.bind((host, port))
        tcp_socket = tcp_socket_init(host, port)
        tcp_socket.listen(1)

    if is_packets_received:
        window['speed'].Update(f'{speed} KB/S')
        window['count'].Update(f'{current} из {total}')
        window[RECEIVE_BUTTON_EVENT].update(disabled=False)
        is_packets_received = False
    
    if event == RECEIVE_BUTTON_EVENT:
        window[RECEIVE_BUTTON_EVENT].update(disabled=True)
        t = Thread(target=receive_packets)
        t.start()
      
        

tcp_socket.close()
udp_socket.close()
