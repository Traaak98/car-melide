# python

from pyproj import Proj, Geod
import numpy as np

publisher_lat = None
publisher_lon = None
subscriber_speed = None
subscriber_steering = None

x0, y0 = 0, 0
lat0 = 48.418075
lon0 = -4.473297

# MyProj = Proj("+proj=utm +zone=31, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
P = Proj(proj='utm', zone=31, ellps='WGS84', preserve_units=True)
G = Geod(ellps='WGS84')

xutm0, yutm0 = P(lon0, lat0)


def subscriber_speed_callback(msg):
    print(msg.keys())  # for debug (to get the keys of the python dict associated to the topic)
    sim.addLog(sim.verbosity_scriptinfos,
               'subscriber received speed : data=' + str(msg['data']))
    speed = msg['data']
    # and apply these commands to the actuators (joints) in CoppeliaSim (/Steering and /FrontMotor)
    sim.setJointTargetVelocity(sim.getObject("/Axe_roues", {}), speed)


def subscriber_steering_callback(msg):
    print(msg.keys())  # for debug (to get the keys of the python dict associated to the topic)
    sim.addLog(sim.verbosity_scriptinfos,
               'subscriber received steering : data=' + str(msg['data']))
    steering = msg['data']
    # and apply these commands to the actuators (joints) in CoppeliaSim (/Steering and /FrontMotor)
    sim.setJointTargetPosition(sim.getObject("/Joint_Servo", {}), steering)


def sysCall_init():
    global publisher_lat, publisher_lon, subscriber_speed, subscriber_steering, x0, y0
    x0, y0, _ = sim.getObjectPosition(sim.getObject('/Chassis', {}), -1)
    sim.addLog(sim.verbosity_scriptinfos, "après calculs, xutm0 = %f, yutm0 = %f" % (xutm0, yutm0))
    # Prepare the float32 publisher and subscriber
    if simROS2:
        publisher_lat = simROS2.createPublisher('/lat', 'std_msgs/msg/Float64')
        publisher_lon = simROS2.createPublisher('/lon', 'std_msgs/msg/Float64')
        subscriber_speed = simROS2.createSubscription('/speed', 'std_msgs/msg/Float32', 'subscriber_speed_callback')
        subscriber_steering = simROS2.createSubscription('/steering', 'std_msgs/msg/Float32', 'subscriber_steering_callback')


def sysCall_actuation():
    global publisher_lat, publisher_lon
    # Send an updated distance for the front obstacle
    # front_sonar = sim.getObject("/FrontSonar")
    # result, distance, detected_point, detected_object_handle, detected_object_normal = sim.handleProximitySensor (front_sonar)

    # calcul du bruit artificiel
    theta = np.random.uniform(0., 2*np.pi)
    sigma = 2.
    r = np.random.normal(sigma/2, sigma)
    # sim.addLog(sim.verbosity_scriptinfos, "bruit calculé, theta = %f, r = %f" % (theta, r))

    x, y, _ = sim.getObjectPosition(sim.getObject('/Chassis', {}), -1)
    x += r * np.cos(theta)
    y += r * np.sin(theta)
    dx = x - x0
    dy = y - y0

    xutm = xutm0 + dx
    yutm = yutm0 + dy

    lon, lat = P(xutm, yutm, inverse=True)
    if simROS2:
        simROS2.publish(publisher_lat, {'data': lat})
        simROS2.publish(publisher_lon, {'data': lon})
        # sim.addLog(sim.verbosity_scriptinfos, "position gps envoyée, latitude = %f°, longitude = %f°" % (lat, lon))
    pass


def sysCall_cleanup():
    global publisher_lat, publisher_lon, subscriber_speed, subscriber_steering
    # Following not really needed in a simulation script (i.e. automatically shut down at simulation end):
    if simROS2:
        simROS2.shutdownPublisher(publisher_lat)
        simROS2.shutdownPublisher(publisher_lon)
