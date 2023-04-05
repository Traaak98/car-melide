"""
Serveur simulant le fonctionnement du robot.

Il reçoit les informations de contrôle du client, active les actionneurs en conséquence
et renvoie les informations des capteurs au client.
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

PORT = 5397

def sysCall_thread() -> None:
    sim.addLog(sim.verbosity_scriptinfos, "Server started")
    sim.setThreadAutomaticSwitch(False)
    host = socket.gethostname()
    port = PORT
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    c, addr = s.accept()
    sim.addLog(sim.verbosity_scriptinfos, "Connection from: " + str(addr))

    chassis = sim.getObject('/Chassis', {})
    axe_moteur = sim.getObject('/Axe_roues', {})
    while True:
        
        position = sim.getObjectPosition(chassis, -1)
        orientation = sim.getObjectOrientation(chassis, -1)
        
        velocity=sim.getJointVelocity(axe_moteur)
        
        objective=sim.getJointTargetVelocity(axe_moteur)
        sim.addLog(sim.verbosity_scriptinfos, objective)

        message = "x: %.3f, y: %.3f, theta: %.3f, omega: %.3f"%(position[0],position[1],orientation[0], velocity)
        sim.addLog(sim.verbosity_scriptinfos, message)
        c.send(message.encode())

        data = c.recv(1024).decode()
        if data == "exit":
            break
        else:
            #format : STEERING: 0.0,SPEED: 0.0
            [steering, speed] = data.split(',')
            steering = float(steering.split(':')[1])
            speed = float(speed.split(':')[1])
            jointSteering = sim.getObject('/Joint_Servo', {})
            sim.setJointTargetPosition(jointSteering, -steering)
            sim.setJointTargetVelocity(axe_moteur, speed)
        sim.switchThread()
    c.close()

if __name__ == '__main__':
    sysCall_thread()
