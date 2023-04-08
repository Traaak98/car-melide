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
import numpy as np
from math import pi
from pygame.locals import *
from Regulateur import regulator as reg
import matplotlib.pyplot as plt
from time import time
import threading

STEERING, SPEED = 0, 0
x,y = 0,0
clavier = False

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

def fig(f,xlim, ylim, step, *args):
    global x, y

    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid()

    Lx, Ly = [], []

    while True:
        Lx.append(x); Ly.append(y)
        ax.clear()
        ax.plot(Lx, Ly, 'r')
        ax.plot(x, y, 'bo')
        ax.grid()
        reg.plot_vector_field(ax, f, xlim, ylim, step, *args)
    
        plt.pause(0.1)
    
    plt.show()

def client() -> None:
    """Client function
    """
    global STEERING, SPEED, x, y, clavier

    sock = socket.socket()
    sock.connect((HOST, PORT))

    speedmax = 50
    run = True
    while run:
        data = sock.recv(1024).decode()
        [x, y, theta, omega] = data.split(',')
        x = float(x.split(':')[1])
        y = float(y.split(':')[1])
        theta = float(theta.split(':')[1])-pi/2
        omega = -float(omega.split(':')[1])

        if clavier:
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
            screen.fill((159, 182, 205))
        
        else:
            vec=reg.circuit(x,y,(-5,3), (4,2), 4, 2)
            vec = (vec/np.linalg.norm(vec))*50 if np.linalg.norm(vec) != 0 else vec
            STEERING, SPEED = reg.regule_vector([x,y,theta,omega], vec)


        STEERING = min(max(STEERING, -np.pi/3), np.pi/3)
        SPEED    = min(max(SPEED, -speedmax), speedmax)

        message = "STEERING:" + str(STEERING) + ",SPEED:" + str(SPEED)
        sock.send(message.encode())

    sock.close()

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    HOST = socket.gethostname()
    PORT = 8080
    
    choix = input("Choix de la commande (1: clavier, 2: autonome): ")
    if choix == "1":
        print("Commande clavier")
        FONT = pygame.font.Font(None, 24)
        WINDOW_SIZE = (320, 240)

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
        screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Commande')

        clavier = True
    else:
        print("Commande autonome")
        clavier = False
    
    threading.Thread(target=client).start()
    fig(reg.circuit_plot, (-10,10), (-10,10), 0.7, (-5,3), (4,2), 4, 2)
