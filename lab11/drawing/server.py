import socket

import cv2
import numpy as np

img = np.zeros(shape=[360, 640, 3], dtype=np.uint8)
color = (255, 0, 255)
thickness = 4
cv2.namedWindow(winname="Server")

HOST = "127.0.0.1"
PORT = 12001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cv2.imshow("Server", img)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()


if __name__ == '__main__':
    while True:
        cv2.imshow("Server", img)
        if cv2.waitKey(10) == 27:
            break
        data = conn.recv(1024)
        if data != b'':
            for ends in data.decode('utf-8').split(':'):
                if ends == '':
                    break
                lx, ly, rx, ry = ends.split()
                cv2.line(img, (int(lx), int(ly)), (int(rx), int(ry)), color, thickness=thickness)


    conn.close()
    cv2.destroyAllWindows()