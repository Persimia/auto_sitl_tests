import mavlink_helper as mh
import gazebo_helper as gh
import utilities as ut
import process_manager as pm
import sdf_modifier as sm
import os

test_name = None
state_message_dict = {
    "Default": "LASS: Entering Default state",
    "Lass": "LASS: Entering Lass state",
    "LeadUp": "LASS: Entering LeadUp state",
    "CoastIn": "LASS: Entering CoastIn state",
    "WindDown": "LASS: Entering WindDown state",
    "Vegetable": "LASS: Entering Vegetable state",
    "WindUp": "LASS: Entering WindUp state",
    "CoastOut": "LASS: Entering CoastOut state",
    "Recover": "LASS: Entering Recover state",
}

def init_mav():
    mh.initiate_connection()

def wait_for_start_sequence():
    mh.wait_for_prearm_pass()

def wait_for_takeoff(altitude: float = 35, alt_tol = .1, timeout: float = 30):
    time_start = gh.get_time()
    mh.enter_mode(4)
    mh.arm_throttle()
    mh.takeoff(altitude)
    print("Waiting for altitude...")
    while gh.get_time() - time_start < timeout: 
        cur_alt = mh.get_local_position_neu()['z']
        # print(cur_alt)
        if abs(cur_alt - altitude) < alt_tol:
            mh.send_rc_override(3,1500)
            return
    print("Altitude message timeout failure!")

def sim_speedup(speedup_val: float):
    mh.change_parameter('SIM_SPEEDUP',speedup_val)

def inject_fault(fault_msg):
    # disattached: disables the attached signal
    # disdetached: disables the detached signal
    # noattach<idx>: disables the cup <idx> suction force
    # nodetach<idx>: disables detach of cup <idx>
    gh.inject_fault(fault_msg)

def track_object(object_name):
    gh.track_object(object_name)

def start_attach_maneuver():
    # TODO add wait for confirmations or feedback
    mh.send_rc_override(3,1500) # set throttle to neutral
    mh.enter_mode(29) # enter lass mode
    mh.send_rc_override(9,2000) # set attachdetach to high


def start_detach_maneuver():
    mh.send_rc_override(9,1000)

def wait_for_state(state_key):
    mh.wait_for_statustext(state_message_dict[state_key])

def save_run_data():
    global test_name
    ut.save_run_data(test_name)

def exit_now():
    raise(Exception("Exit called by sequence"))

processes = None
from paths_and_constants import *
def startup(name_of_test, show_gazebo: bool = False, sdf_mod_list: dict = {}):
    global processes, test_name
    test_name = name_of_test
    ut.copy_param_file(original_param_file_path, param_file_path)
    sm.generate_world_file(original_world_file_dir, original_world_file_name, world_file_path, sdf_mod_list)
    commands = pm.make_commands(sitl_data_dir, param_file_path, microros_agent_path, ros_bridge_config_path, model_dir, world_file_path, gazebo_data_dir, show_gazebo)
    processes = pm.start_processes(commands)

def spin():
    global processes
    for process in processes:
        process.wait()

import time
def gust(duration_s, east, north, up):
    gh.linear_wind(east, north, up)
    time_start = time.time()
    while time.time() - time_start < duration_s:
        time.sleep(.1)
    gh.linear_wind(0, 0, 0)
