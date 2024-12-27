from sdf_modifier import generate_world_file
from process_manager import make_commands, start_processes
from mavlink_helper import initiate_connection, enter_mode, wait_for_prearm_pass

original_world_file_dir = "/home/skemp32/ros2_ws/src/sitl_models/worlds/"
original_world_file_name = "js_turbine.sdf"
world_file_path = f"/home/skemp32/ros2_ws/src/auto_sitl_tests/Temp/worlds/world.sdf"

generate_world_file(original_world_file_dir, original_world_file_name, world_file_path)

sitl_data_dir = "/home/skemp32/ros2_ws/src/auto_sitl_tests/Temp/sitl-data"
param_file_path = "/home/skemp32/ros2_ws/src/sitl_models/config/gazebo-doe.parm"
microros_agent_path = "/home/skemp32/ros2_ws/install/micro_ros_agent/lib/micro_ros_agent/micro_ros_agent"
ros_bridge_config_path = "/home/skemp32/ros2_ws/src/sitl_models/config/doe_lidar_bridge.yaml"
model_dir = "/home/skemp32/ros2_ws/src/sitl_models/models"

commands = make_commands(sitl_data_dir, param_file_path, microros_agent_path, ros_bridge_config_path, model_dir, world_file_path)
processes = start_processes(commands)

# connect to MAVlink
initiate_connection()
wait_for_prearm_pass()


enter_mode(4)

# wait for processes to start

# start ROS2 publishers and subscribers
# start gazebo transport layer?
# run sequence

# Wait for all processes to finish (if needed, or let cleanup take care of termination)
for process in processes:
    process.wait()