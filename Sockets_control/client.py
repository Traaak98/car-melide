"""
Client permettant d'envoyer les commandes de contrôle au robot.

"""

__author__ = "Ludovic Mustière"
__copyright__ = "Copyright 2023, La Car-Mélide"
__credits__ = ["Ludovic Mustière", "Gwendal Crequer", "Clara Gondot",
               "Apolline de Vaulchier du Deschaux"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Ludovic Mustière"
__email__ = "ludovic.mustiere@ensta-bretagne.org"
__status__ = "Production"

import socket
import os
import pygame
from math import pi
from pygame.locals import *

STEERING, SPEED = 0, 0

def display(str : str, x=0, y=0) -> None:
    """Display text on the screen

    Args:
        str (str): Text to display
        x (int, optional): x increment from center of the window. Defaults to 0.
        y (int, optional): y increment from center of the window. Defaults to 0.
    """
    text = FONT.render(str, True, (255, 255, 255), (159, 182, 205))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx + x
    textRect.centery = screen.get_rect().centery + y

    screen.blit(text, textRect)
    pygame.display.update()

def client() -> None:
    """Client function
    """
    global STEERING, SPEED

    sock = socket.socket()
    sock.connect((HOST, PORT))

    speedmax = 30
    run = True
    while run:
        data = sock.recv(1024).decode()
        [x, y, theta, omega] = data.split(',')
        x = float(x.split(':')[1])
        y = float(y.split(':')[1])
        theta = float(theta.split(':')[1])
        omega = float(omega.split(':')[1])

        display("STEERING : " + str(round(STEERING,4)), y=-20)
        display("SPEED : " + str(round(SPEED,4)), y=20)
        display("RIGHT: +Steering", x=-WINDOW_SIZE[0]//4, y=-100)
        display("LEFT: -Steering", x=WINDOW_SIZE[0]//4, y=-100)
        display("UP: +Speed", x=-WINDOW_SIZE[0]//4, y=-80)
        display("DOWN: -Speed", x=WINDOW_SIZE[0]//4, y=-80)
        display("ESC: Quit", y=100)

        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            run = False
            message = "exit"
            sock.send(message.encode())
        elif keys[K_RIGHT]:
            STEERING += 0.01
        elif keys[K_LEFT]:
            STEERING -= 0.01
        elif keys[K_UP]:
            SPEED += 0.1
        elif keys[K_DOWN]:
            SPEED -= 0.1

        if STEERING > 180:
            STEERING = 180
        elif STEERING < -180:
            STEERING = -180

        if SPEED > speedmax:
            SPEED = speedmax
        elif SPEED < -speedmax:
            SPEED = -speedmax

        message = "STEERING:" + str(STEERING) + ",SPEED:" + str(SPEED)
        sock.send(message.encode())

        screen.fill((159, 182, 205))

    sock.close()

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    HOST = socket.gethostname()
    PORT = 5398
    FONT = pygame.font.Font(None, 24)
    WINDOW_SIZE = (320, 240)

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Commande')

    client()
