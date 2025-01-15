import fault_scenarios as fs
import process_manager as pm
import sequence_helper as sh
import sys

def soft_exit(signal_received=None, frame=None):
    print("=========== ERROR HERE ============")
    print(sys.exc_info())
    # time.sleep(10)
    pm.cleanup(None, None)
    print('Saving run data')
    sh.save_run_data()
    exit(1)

try:
    # run sequence
    # fs.quickstart()
    fs.suction_detach_delay()
    # fs.s0_0_0()
    # fs.s0_0_1()
    # fs.s3_3_2()
    # fs.testing()
    # time.sleep(30)

# gz sim -r -v 4 --playback "/home/skemp32/ros2_ws/src/auto_sitl_tests/Temp/gz-data"

except:
    soft_exit()
    

