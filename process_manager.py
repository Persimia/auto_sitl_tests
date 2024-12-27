import subprocess
import signal
import sys

processes = []

def make_commands(sitl_data_dir, param_file_path, microros_agent_path, ros_bridge_config_path, model_dir, world_file_path):
    return [
        f"GZ_SIM_RESOURCE_PATH={model_dir}:$GZ_SIM_RESOURCE_PATH; gz sim -v4 -r {world_file_path}",
        f"ros2 run ros_gz_bridge parameter_bridge --ros-args -p config_file:={ros_bridge_config_path}",
        f"{microros_agent_path} udp4 --middleware dds --verbose 4 --port 2019 --ros-args -r __node:=micro_ros_agent -r __ns:=/",
        f"cd {sitl_data_dir}; sim_vehicle.py -v ArduCopter --model=json --add-param-file={param_file_path} --speedup=1 --slave=0 --sim-address=127.0.0.1 --instance=0 --enable-dds -A --synthetic-clock -A --serial5=sim:sf45b"
    ]

# Function to handle cleanup on script termination
def cleanup(signum, frame):
    print("Cleaning up...")
    for p in processes:
        try:
            p.terminate()  # Terminate the process
            p.wait(timeout=10)  # Wait with a timeout of 10 seconds
        except subprocess.TimeoutExpired:
            print(f"Process {p.pid} did not terminate in time. Forcefully killing it.")
            p.kill()  # Forcefully kill the process if it times out
        except Exception as e:
            print(f"Error terminating process: {e}")
    sys.exit(0)

def start_processes(commands):
    # Register signal handler to clean up on interrupt (Ctrl+C)
    signal.signal(signal.SIGINT, cleanup)

    # Execute each command in a new subprocess and store the process references
    for command in commands:
        process = subprocess.Popen(command, shell=True)
        processes.append(process)

    return processes
    
