# python

publisher_lat = None
publisher_lon = None
subscriber_speed = None
subscriber_steering = None


def subscriber_speed_callback(msg):
    print(msg.keys())  # for debug (to get the keys of the python dict associated to the topic)
    sim.addLog(sim.verbosity_scriptinfos,
               'subscriber received speed : data=' + str(msg['data']))
    speed = msg['data']
    # and apply these commands to the actuators (joints) in CoppeliaSim (/Steering and /FrontMotor)
    sim.setJointTargetVelocity(sim.getObject("/Axes_roues"), speed)


def subscriber_steering_callback(msg):
    print(msg.keys())  # for debug (to get the keys of the python dict associated to the topic)
    sim.addLog(sim.verbosity_scriptinfos,
               'subscriber received steering : data=' + str(msg['data']))
    steering = msg['data']
    # and apply these commands to the actuators (joints) in CoppeliaSim (/Steering and /FrontMotor)
    sim.setJointTargetPosition(sim.getObject("/Joint_Servo"), steering)


def sysCall_init():
    global publisher_lat, publisher_lon, subscriber_speed, subscriber_steering
    # Prepare the float32 publisher and subscriber
    if simROS2:
        publisher_lat = simROS2.createPublisher('/lat', 'std_msgs/msg/Float32')
        publisher_lon = simROS2.createPublisher('/lon', 'std_msgs/msg/Float32')
        subscriber_speed = simROS2.createSubscription('/speed', 'std_msgs/msg/Float32', 'subscriber_speed_callback')
        subscriber_steering = simROS2.createSubscription('/steering', 'std_msgs/msg/Float32', 'subscriber_steering_callback')


def sysCall_actuation():
    global publisher_lat, publisher_lon, subscriber_speed, subscriber_steering
    # Send an updated distance for the front obstacle
    # front_sonar = sim.getObject("/FrontSonar")
    # result, distance, detected_point, detected_object_handle, detected_object_normal = sim.handleProximitySensor (front_sonar)
    lat = 0
    lon = 0
    if simROS2:
        simROS2.publish(publisher_lat, {'data': lat})
        simROS2.publish(publisher_lon, {'data': lon})
    pass


def sysCall_cleanup():
    global publisher_lat, publisher_lon, subscriber_speed, subscriber_steering
    # Following not really needed in a simulation script (i.e. automatically shut down at simulation end):
    if simROS2:
        simROS2.shutdownPublisher(publisher_lat)
        simROS2.shutdownPublisher(publisher_lon)
