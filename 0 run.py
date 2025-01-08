import fault_scenarios as fs
import process_manager as pm
import sequence_helper as sh
import sys  , time, signal

def soft_exit(signal_received=None, frame=None):
    print("=========== ERROR HERE ============")
    print(sys.exc_info())
    # time.sleep(10)
    pm.cleanup(None, None)
    print('Saving run data')
    sh.save_run_data()
    exit(1)

# signal.signal(signal.SIGINT, soft_exit)

try:
    # run sequence
    # fs.s0_0_0()
    fs.quickstart()
    # fs.testing()
    # time.sleep(30)
    


# gz sim -r -v 4 --playback "/home/skemp32/ros2_ws/src/auto_sitl_tests/Temp/gz-data"

except:
    soft_exit()
    

