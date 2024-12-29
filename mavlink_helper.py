from pymavlink import mavutil
import time
master = None

# connect to SITL
def initiate_connection():
    global master
    start_time = time.time()
    while True:
        try:
            if time.time() - start_time > 10:
                raise TimeoutError
            master = mavutil.mavlink_connection('tcp:127.0.0.1:5762')
            print("Waiting for heartbeat")
            master.wait_heartbeat()
            print("Connected to system:", master.target_system, ", component:", master.target_component)
            request_datastreams()
            break
        except ConnectionRefusedError:
            print('Retrying mav connection')
            time.sleep(1)
        except TimeoutError:
            print('Timeout exceeded')
            break
        except Exception as e:
            print(e)
            break

def request_datastreams():
    global master
    message_id = mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS  # SYS_STATUS message ID
    interval_us = 1000000  # Interval in microseconds (1,000,000 us = 1 second = 1 Hz)
    print("Setting SYS_STATUS message interval...")
    master.mav.command_long_send(
        master.target_system, 
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 
        0,  # Confirmation
        message_id,  # Message ID
        interval_us,  # Interval in microseconds
        0, 0, 0, 0, 0  # Unused parameters
    )
    message_id = mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED   # LOCAL_POSITION_NED  message ID
    interval_us = 100  # Interval in microseconds (1,000,000 us = 1 second = 1 Hz)
    print("Setting LOCAL_POSITION_NED  message interval...")
    master.mav.command_long_send(
        master.target_system, 
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 
        0,  # Confirmation
        message_id,  # Message ID
        interval_us,  # Interval in microseconds
        0, 0, 0, 0, 0  # Unused parameters
    )

def wait_for_prearm_pass():
    global master
    # Loop to monitor system status
    print("Waiting for prearm check to pass...")
    while True:
        # Fetch the next message
        msg = master.recv_match(type='SYS_STATUS', blocking=True)
        if msg:
            if msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_PREARM_CHECK:
                print("PREARM READY!!!")
                break


def enter_mode(mode_num: int): 
    global master
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0, # confirmation
        1, # param1 (MAV_MODE_FLAG_CUSTOM_MODE_ENABLED)
        mode_num, # param2 (flightmode number)
        0, # param3
        0, # param4
        0, # param5
        0, # param6
        0) # param7

def arm_throttle():
    global master
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Command ID for arming or disarming
        0,  # confirmation (0 means no confirmation)
        1,  # param1: 1 for arming, 0 for disarming
        0,  # param2: unused in this command
        0,  # param3: unused in this command
        0,  # param4: unused in this command
        0,  # param5: unused in this command
        0,  # param6: unused in this command
        0   # param7: unused in this command
    )

def takeoff(altitude: float = 15):
    global master
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,  # Command ID for takeoff
        0,  # confirmation (0 means no confirmation)
        0,  # param1: unused (set to 0)
        0,  # param2: unused (set to 0)
        0,  # param3: unused (set to 0)
        0,  # param4: unused (set to 0)
        0,  # param5: unused (set to 0)
        0,  # param6: target altitude in meters
        altitude   # param7: unused (set to 0)
    )

def get_local_position_neu():
    global master
    # Loop to monitor system status
    print("Waiting for position...")
    while True:
        # Fetch the next message
        msg = master.recv_match(type='LOCAL_POSITION_NED', blocking=True)
        if msg:
            pos_neu = {
                'x': msg.x,
                'y': msg.y,
                'z': -msg.z,
                'vx': msg.vx,
                'vy': msg.vy,
                'vz': -msg.vz,
            }
            return pos_neu
