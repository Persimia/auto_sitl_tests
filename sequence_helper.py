import mavlink_helper as mh
import gazebo_helper as gh

def wait_for_start_sequence():
    mh.initiate_connection()
    mh.wait_for_prearm_pass()

def wait_for_takeoff(altitude: float = 35, alt_tol = .1, timeout: float = 30):
    time_start = gh.get_time()
    mh.enter_mode(4)
    mh.arm_throttle()
    mh.takeoff(altitude)
    while gh.get_time() - time_start < timeout: 
        cur_alt = mh.get_local_position_neu()['z']
        print(cur_alt)
        if abs(cur_alt - altitude) < alt_tol:
            return
    print("Altitude message timeout failure!")
