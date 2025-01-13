import gz.transport13 as transport  # Import the Gazebo Transport library
from gz.msgs10.clock_pb2 import Clock
from gz.msgs10.stringmsg_pb2 import StringMsg
from gz.msgs10.cameratrack_pb2 import CameraTrack
from gz.msgs10.wind_pb2 import Wind

import time, signal


# def wait_for_clock_msg(timeout: float = 5):
start_time = time.time()
node = transport.Node()
clock_topic = "/clock"
fault_topic = "/failure_topic"
track_topic = "/gui/track"
wind_topic = "/world/js_turbine/wind"


sim_time_s = 0
msg_recieved = False


# Callback function to handle received messages
def on_message_received(msg):
    global sim_time_s, msg_recieved
    sim_time_s = msg.sim.sec + msg.sim.nsec / (10**9)
    msg_recieved = True

success = node.subscribe(Clock, clock_topic, on_message_received)
if not success:
    print(f"Failed to subscribe to topic: {clock_topic}")
    signal.raise_signal(signal.SIGINT)

fault_publisher = node.advertise(fault_topic, StringMsg)
if not fault_publisher:
    print(f"Failed to advertise to topic: {fault_topic}")
    signal.raise_signal(signal.SIGINT)

track_publisher = node.advertise(track_topic, CameraTrack)
if not track_publisher:
    print(f"Failed to advertise to topic: {track_topic}")
    signal.raise_signal(signal.SIGINT)

wind_publisher = node.advertise(wind_topic, Wind)
if not wind_publisher:
    print(f"Failed to advertise to topic: {wind_topic}")
    signal.raise_signal(signal.SIGINT)

def get_time(timeout:float = 5):
    global sim_time_s, msg_recieved
    start_time = time.time()
    while time.time()-start_time < timeout:
        if msg_recieved:
            return sim_time_s
    print('Timeout. Failed to get sim time.')
    signal.raise_signal(signal.SIGINT)

def inject_fault(failure_msg):
    global fault_publisher
    fault_message = StringMsg()
    fault_message.data = failure_msg
    fault_publisher.publish(fault_message)

def track_object(object_name):
    global track_publisher
    msg = CameraTrack()
    msg.follow_target.name = object_name
    msg.follow_offset.x = -3
    msg.follow_offset.z = 2
    msg.follow_pgain = 0.01
    msg.track_mode= 2

    track_publisher.publish(msg)

def linear_wind(east, north, up):
    global wind_publisher
    msg = Wind()

    msg.enable_wind = True
    msg.linear_velocity.x = east # east
    msg.linear_velocity.y = north # north
    msg.linear_velocity.z = up

    wind_publisher.publish(msg)



