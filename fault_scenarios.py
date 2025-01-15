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
    sh.wait_for_takeoff(29)
    sh.sim_speedup(1)
    sh.spin()

def suction_detach_delay():
    test_name = "1 Suction detach delay"
    sdf_mod_list = [
        {
            "model" : "jumping_spider_controls",
            "submodel" : "jumping_spider",
            "component_dicts_list" : [{
                "component" : "plugin",
                "name" : "SuctionPlugin",
                "new_name" : "SuctionPlugin",
                "action" : "modify",
                "prop_dict" : {
                    "suction_delay1":"50",
                    "suction_delay2":"50",
                    "detach_delay1":"50",
                    "detach_delay2":"50",
                }
            }]
        }
    ]
    sh.startup(test_name, show_gazebo=True, sdf_mod_list=sdf_mod_list)
    sh.init_mav()
    sh.sim_speedup(10)
    sh.track_object(main_object_name)
    sh.wait_for_start_sequence()
    sh.wait_for_takeoff(29)
    sh.sim_speedup(1)
    sh.spin()

def s0_0_1():
    test_name = "0.0.1 Right collision disabled" 
    sdf_mod_list = [
        {
            "model" : "jumping_spider_controls",
            "submodel" : "jumping_spider::right_pitch_link_1",
            "component_dicts_list" : [{
                "component" : "collision",
                "name" : "right_suction_collision",
                "new_name" : "right_suction_collision",
                "action" : "remove",
                "prop_dict" : {
                }
            }]
        }
    ]
    sh.startup(test_name, show_gazebo=True, sdf_mod_list=sdf_mod_list)
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
    sh.start_attach_maneuver()
    sh.wait_for_state("Vegetable")
    sh.start_detach_maneuver()
    sh.wait_for_state("Lass")
    sh.exit_now()

def s3_3_2():
    test_name = "3.3.2 Gust during LeadUp"
    sh.startup(test_name, show_gazebo=True)
    sh.init_mav()
    sh.sim_speedup(10)
    sh.track_object(main_object_name)
    sh.wait_for_start_sequence()
    sh.wait_for_takeoff(35)
    sh.sim_speedup(1)
    sh.start_attach_maneuver()
    sh.wait_for_state("LeadUp")
    #send 10s gust
    sh.gust(10,80,0,0)
    sh.wait_for_state("Vegetable")
    sh.start_detach_maneuver()
    sh.wait_for_state("Lass")
    # sh.exit_now()
    sh.spin()
    
def testing():
    test_name = "0 testing"
    sh.startup(test_name, show_gazebo=True)
    