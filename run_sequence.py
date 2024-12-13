from sdf_modifier import generate_world_file
from process_manager import make_commands, start_processes
import os


original_world_file_dir = "/home/skemp32/ros2_ws/src/sitl_models/worlds/"
original_world_file_name = "js_turbine.sdf"
world_file_path = f"/home/skemp32/ros2_ws/src/gazebo_testing/Temp/worlds/world.sdf"

generate_world_file(original_world_file_dir, original_world_file_name, world_file_path)

sitl_data_dir = "/home/skemp32/ros2_ws/src/gazebo_testing/Temp/sitl-data"
param_file_path = "/home/skemp32/ros2_ws/src/sitl_models/config/gazebo-doe.parm"
microros_agent_path = "/home/skemp32/ros2_ws/install/micro_ros_agent/lib/micro_ros_agent/micro_ros_agent"
ros_bridge_config_path = "/home/skemp32/ros2_ws/src/sitl_models/config/doe_lidar_bridge.yaml"
model_dir = "/home/skemp32/ros2_ws/src/sitl_models/models"


commands = make_commands(sitl_data_dir, param_file_path, microros_agent_path, ros_bridge_config_path, model_dir, world_file_path)
start_processes(commands)