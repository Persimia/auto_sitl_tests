from pymavlink import mavutil
import schedule
import threading
import time
period = 1 # period in s that schedule is called
master = None
rc_override_array = [0] * 18

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
        21196,  # param2: 0: arm-disarm unless prevented by safety checks, 21196: force arming or disarming
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

def format_param_id(param):
    param_encoded = param.encode('utf-8') + b'\x00'
    param_encoded = param_encoded[0:16]
    return param_encoded

def change_parameter(param_id: str, param_value: float, timeout: float = 1, retries: int = 5):
    global master
    formatted_param_id = format_param_id(param_id)
    
    master.mav.param_set_send(
        master.target_system,
        master.target_component,
        formatted_param_id,  # Parameter name (must be a 16-byte string)
        param_value,                 # Parameter value (as float)
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32  # Parameter type
    )
    message = master.recv_match(type='PARAM_VALUE', blocking=True, timeout = timeout)
    if message:
        print(f"Parameter {message.param_id} set to {message.param_value}")
    else:
        print(f"FAILURE TO SET PARAMETER {param_id} to {param_value}")

def close():
    global master
    master.close()

def send_rc_override(channel, value):
    global master
    global rc_override_array
    # RC channels: 1 to 8 are standard; 9+ are optional
    # Set unused channels to 0 (no override)
    rc_override_array[channel-1] = value

def clear_rc_override():
    global rc_override_array
    rc_override_array = [0] * 18


def idle_work():
    global master
    global rc_override_array

    if not master:
        return
    
    if any(x != 0 for x in rc_override_array):  
        # Send MAVLink RC_CHANNELS_OVERRIDE message
        master.mav.rc_channels_override_send(
            master.target_system,    # Target system ID
            master.target_component, # Target component ID
            *rc_override_array                 # RC channel values
        )

stop_event = threading.Event()
def run_scheduler():
    while not stop_event.is_set():
        schedule.run_pending()

schedule.every(period).seconds.do(idle_work)
idle_thread = threading.Thread(target=run_scheduler, daemon=False)
idle_thread.start()

def wait_for_statustext(text_to_find):
    while True:
        # Wait for the next message
        message = master.recv_match(type='STATUSTEXT', blocking=True)
        if message is not None:
            text = message.text
            if text_to_find in text:
                break
            
