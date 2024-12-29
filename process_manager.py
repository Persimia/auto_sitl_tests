import subprocess
import signal
import sys, os, psutil

processes = []

def make_commands(sitl_data_dir, param_file_path, microros_agent_path, ros_bridge_config_path, model_dir, world_file_path):
    return [
        f"GZ_SIM_RESOURCE_PATH={model_dir}:$GZ_SIM_RESOURCE_PATH; gz sim -v4 -r {world_file_path}",
        f"ros2 run ros_gz_bridge parameter_bridge --ros-args -p config_file:={ros_bridge_config_path}",
        f"{microros_agent_path} udp4 --middleware dds --verbose 4 --port 2019 --ros-args -r __node:=micro_ros_agent -r __ns:=/",
        f"cd {sitl_data_dir}; sim_vehicle.py -v ArduCopter --model=json --add-param-file={param_file_path} --speedup=1 --slave=0 --sim-address=127.0.0.1 --instance=0 --enable-dds -A --synthetic-clock -A --serial5=sim:sf45b"
    ]


def kill_proc_tree(pid, sig=signal.SIGINT, include_parent=True,
                   timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callback function which is
    called as soon as a child terminates.
    """
    # assert pid != os.getpid(), "won't kill myself"
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        try:
            p.send_signal(sig)
        except psutil.NoSuchProcess:
            pass
    gone, alive = psutil.wait_procs(children, timeout=timeout,
                                    callback=on_terminate)
    return (gone, alive)

# Function to handle cleanup on script termination
def cleanup(signum, frame):
    print("Cleaning up...")
    # for p in processes:
    kill_proc_tree(os.getpid(), include_parent=False)
    # all_processes = []
    # for p in processes:
    #     all_processes.append(p)
    #     pp = psutil.Process(p.pid)
    #     child_pid = pp.children(recursive=True)
    #     all_processes+=child_pid
    # print(all_processes)
    # for p in all_processes:
    #     pid = p.pid
    #     try:
    #         print("Terminating...")
    #         p.terminate()
    #         p.wait(timeout=10)  # Wait with a timeout of 10 seconds
    #     except subprocess.TimeoutExpired:
    #         print(f"Process {p.pid} did not terminate in time. Forcefully killing it.")
    #         p.kill()
    #     except Exception as e:
    #         print(f"Error terminating process: {e}")
    #     finally:
    #         print(f"{pid} is dead")
    exit(0)

def start_processes(commands):
    # Register signal handler to clean up on interrupt (Ctrl+C)
    signal.signal(signal.SIGINT, cleanup)

    # Execute each command in a new subprocess and store the process references
    i = 0
    for command in commands:
        process = subprocess.Popen(command, shell=True, start_new_session=True)
        # if i < 1:
        #     os.setpgrp(process.pid, 0)
        # else:
        #     os.setpgrp(process.pid, os.getpgid(processes[0]))
        processes.append(process)
        i+=1

    return processes
    
