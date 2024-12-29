import gz.transport13 as transport  # Import the Gazebo Transport library
from gz.msgs10.clock_pb2 import Clock
import time, signal


# def wait_for_clock_msg(timeout: float = 5):
start_time = time.time()
node = transport.Node()
sub_topic = "/clock"
sim_time_s = 0
msg_recieved = False

# Callback function to handle received messages
def on_message_received(msg):
    global sim_time_s, msg_recieved
    sim_time_s = msg.sim.sec + msg.sim.nsec / (10**9)
    msg_recieved = True

success = node.subscribe(Clock, sub_topic, on_message_received)
if not success:
    print(f"Failed to subscribe to topic: {sub_topic}")
    signal.raise_signal(signal.SIGINT)

def get_time(timeout:float = 5):
    global sim_time_s, msg_recieved
    start_time = time.time()
    while time.time()-start_time < timeout:
        if msg_recieved:
            return sim_time_s
    print('Timeout. Failed to get sim time.')
    signal.raise_signal(signal.SIGINT)