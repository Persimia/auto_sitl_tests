import sequence_helper as sh
from paths_and_constants import main_object_name

#s for scenario in function name because function names can't just be numbers
def quickstart():
    test_name = "0 Quickstart"
    sh.startup(test_name, show_gazebo=True)
    sh.init_mav()
    sh.sim_speedup(10)
    sh.track_object(main_object_name)
    sh.wait_for_start_sequence()
    sh.wait_for_takeoff(35)
    sh.sim_speedup(1)
    sh.spin()

def s0_0_0():
    test_name = "0.0.0 Normal sequence no faults"
    sh.startup(test_name, show_gazebo=True)
    sh.init_mav()
    sh.sim_speedup(10)
    sh.track_object(main_object_name)
    sh.wait_for_start_sequence()
    sh.wait_for_takeoff(35)
    sh.wait_for_attach_maneuver()
    sh.wait_for_detach_maneuver()
    sh.exit_now()
    
def testing():
    test_name = "0 testing"
    sh.startup(test_name, show_gazebo=True)
    