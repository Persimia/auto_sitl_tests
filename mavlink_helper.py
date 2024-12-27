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
            master.wait_heartbeat()
            print("Connected to system:", master.target_system, ", component:", master.target_component)
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

def wait_for_prearm_pass():
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
