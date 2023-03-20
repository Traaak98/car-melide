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

HOST = socket.gethostname()
PORT = 5400

def sysCall_thread() -> None:
    sim.addLog(sim.verbosity_scriptinfos, "Server started")
    sim.setThreadAutomaticSwitch(False)
    host = HOST
    port = PORT
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    c, addr = s.accept()
    print("Connection from: " + str(addr))
    while True:
        objHandle = sim.getObject('/MainBodyTubeDyn', {})
        p = sim.getObjectPosition(objHandle, -1)
        message = "x: %.3f,y: %.3f,z: %.3f"%(p[0],p[1],p[2])
        sim.addLog(sim.verbosity_scriptinfos, message)
        c.send(message.encode())
        
        data = c.recv(1024).decode()
        sim.addLog(sim.verbosity_scriptinfos, data)
        #format : steering: 0.0, speed: 0.0
        [steering, speed] = data.split(',')
        steering = float(steering.split(':')[1])
        speed = float(speed.split(':')[1])
        jointSteering = sim.getObject('/MainBodyTubeDyn/Steering', {})
        jointSpeed = sim.getObject('/MainBodyTubeDyn/Steering/ForkLeftDyn/FrontMotor', {})
        sim.setJointTargetPosition(jointSteering, steering)
        sim.setJointTargetVelocity(jointSpeed, speed)
        
        sim.switchThread()
    c.close()

if __name__ == '__main__':
    sysCall_thread()
