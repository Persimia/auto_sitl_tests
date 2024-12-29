import sdf_modifier as sm
import process_manager as pm
import sequence_helper as sh
import sys, signal  

try:
    original_world_file_dir = "/home/skemp32/ros2_ws/src/sitl_models/worlds/"
    original_world_file_name = "js_turbine.sdf"
    world_file_path = f"/home/skemp32/ros2_ws/src/auto_sitl_tests/Temp/worlds/world.sdf"

    sm.generate_world_file(original_world_file_dir, original_world_file_name, world_file_path)

    sitl_data_dir = "/home/skemp32/ros2_ws/src/auto_sitl_tests/Temp/sitl-data"
    param_file_path = "/home/skemp32/ros2_ws/src/sitl_models/config/gazebo-doe.parm"
    microros_agent_path = "/home/skemp32/ros2_ws/install/micro_ros_agent/lib/micro_ros_agent/micro_ros_agent"
    ros_bridge_config_path = "/home/skemp32/ros2_ws/src/sitl_models/config/doe_lidar_bridge.yaml"
    model_dir = "/home/skemp32/ros2_ws/src/sitl_models/models"

    commands = pm.make_commands(sitl_data_dir, param_file_path, microros_agent_path, ros_bridge_config_path, model_dir, world_file_path)
    processes = pm.start_processes(commands)

    # run sequence 
    sh.wait_for_start_sequence()
    sh.wait_for_takeoff(35)

    for process in processes:
        process.wait()
except:
    print("=========== ERROR HERE ============")
    print(sys.exc_info())
    pm.cleanup(None, None)
    exit(1)
    

