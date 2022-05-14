import datetime

import PySimpleGUI as gui

from util import *

SEND_BUTTON_EVENT ='Отправить пакеты'

window = gui.Window('TCP отправитель', [
    [gui.Text('Введите IP адрес получателя', size=DEFAULT_GUI_TEXT_SIZE), gui.InputText(DEFAULT_HOST, key='host')],
    [gui.Text('Введите порт получателя', size=DEFAULT_GUI_TEXT_SIZE), gui.InputText(DEFAULT_PORT, key='port')],
    [gui.Text('Введите количество пакетов для отправки', size=DEFAULT_GUI_TEXT_SIZE), gui.InputText('500', key='count')],
    [gui.Button(SEND_BUTTON_EVENT)],
])

while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break

    if event == SEND_BUTTON_EVENT:
        host, port, packets_count = None, None, 0
        try:
            host, port = values['host'], int(values['port'])
            packets_count = int(values['count'])
        except Exception as e:
            print(e)

        if packets_count < 0:
            window['count'].Update('Пожалуйста, введите положительное число.')
            continue

        tcp_socket = None
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((host, port))
            tcp_socket.sendto(bytes(str(packets_count), encoding='utf-8') , (host, port))
            for i in range(packets_count):
                message = f'{int(datetime.datetime.now().timestamp() * 1000)} '
                message += random_string(PACKET_SIZE - len(message))
                tcp_socket.sendto(message.encode(), (host, port))
        except Exception as e:
            print(e)
        finally:
            if tcp_socket is not None:
                tcp_socket.close()