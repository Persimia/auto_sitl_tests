import mavlink_helper as mh
import gazebo_helper as gh
import utilities as ut
import process_manager as pm
import sdf_modifier as sm
import os

test_name = None

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

def wait_for_attach_maneuver():
    # TODO add wait for confirmations or feedback
    mh.send_rc_override(3,1500) # set throttle to neutral
    mh.enter_mode(29) # enter lass mode
    mh.send_rc_override(9,2000) # set attachdetach to high
    mh.wait_for_statustext("LASS: Entering Vegetable state")


def wait_for_detach_maneuver():
    mh.send_rc_override(9,1000)
    mh.wait_for_statustext("LASS: Entering Lass state")

def save_run_data():
    global test_name
    ut.save_run_data(test_name)

def exit_now():
    raise(Exception("Exit called by sequence"))

processes = None
from paths_and_constants import *
def startup(name_of_test, show_gazebo: bool = False):
    global processes, test_name
    test_name = name_of_test
    ut.copy_param_file(original_param_file_path, param_file_path)
    sm.generate_world_file(original_world_file_dir, original_world_file_name, world_file_path)
    commands = pm.make_commands(sitl_data_dir, param_file_path, microros_agent_path, ros_bridge_config_path, model_dir, world_file_path, gazebo_data_dir, show_gazebo)
    processes = pm.start_processes(commands)

def spin():
    global processes
    for process in processes:
        process.wait()