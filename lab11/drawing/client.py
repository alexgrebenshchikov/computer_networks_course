import socket

import cv2
import numpy as np


color = (255, 0, 255)
thickness = 4

def draw_line(rx, ry):
    global lx, ly, img
    cv2.line(img, (lx, ly), (rx, ry), color, thickness=thickness)
    s.send(f'{lx} {ly} {rx} {ry}:'.encode('utf-8'))


def draw_curve(event, rx, ry, flags, param):
    global lx, ly, drawing, img
    match event:
        case cv2.EVENT_LBUTTONDOWN:
            drawing = True
            lx = rx
            ly = ry
        case cv2.EVENT_LBUTTONUP:
            drawing = False
            draw_line(rx, ry)
            lx = rx
            ly = ry
        case cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                draw_line(rx, ry)
                lx = rx
                ly = ry    

HOST = "127.0.0.1"
PORT = 12001

img = np.zeros(shape=[360, 640, 3], dtype=np.uint8)

lx = -1
ly = -1
drawing = False


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


cv2.namedWindow(winname="Client")
cv2.setMouseCallback("Client",
                     draw_curve)


if __name__ == '__main__':
    while True:
        cv2.imshow("Client", img)

        if cv2.waitKey(10) == 27:
            break

    cv2.destroyAllWindows()