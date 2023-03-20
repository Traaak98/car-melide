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
import pygame
from pygame.locals import K_ESCAPE, K_RIGHT, K_LEFT, K_UP, K_DOWN

HOST = socket.gethostname()
PORT = 5400
STEERING = 0
SPEED = 0


def client() -> None:
    """Client function
    """
    global STEERING, SPEED
    
    text = font.render(str, True, (255, 255, 255), (159, 182, 205))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery

    screen.blit(text, textRect)

    pygame.display.update() 
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Python numbers')
    screen.fill((159, 182, 205))

    font = pygame.font.Font(None, 17)
    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    run = True
    while run:
        data = sock.recv(1024).decode()
        if data == 'exit':
            print('Connection closed by the server')
            run = False
        else:
            print('Received from server: ' + data)
            
        display(str(num))
        num += 1

        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            run = False
        elif keys[K_RIGHT]:
            STEERING += 0.1
        elif keys[K_LEFT]:
            STEERING -= 0.1
        elif keys[K_UP]:
            SPEED += 0.1
        elif keys[K_DOWN]:
            SPEED -=0.1
            
    sock.close()

if __name__ == '__main__':
    client()
