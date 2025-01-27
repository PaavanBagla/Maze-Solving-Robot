#! usr/bin/env python

from robot_control_class import RobotControl
import time

rc = RobotControl()
exit = True

def get_readings():
    left_reading = rc.get_laser(719)
    right_reading = rc.get_laser(0)
    return left_reading, right_reading


def move_stop():
    global exit  
    while True:
        dist = rc.get_laser(360)
        if dist == float('inf'):
            left, right = get_readings()
            print("Distance measured from left: ", left)
            print("Distance measured from right: ", right)
            if left == float('inf') and right == float('inf'):
                exit = False
                rc.stop_robot()
                print("Escaped!")
                break
            rc.move_straight()
        elif dist <= 1.2:  # Increased threshold to 1.5 meters
            rc.stop_robot()
            break
        else:
            rc.move_straight()
            print("Distance measured from front: ", dist)
        time.sleep(0.1)  # Small delay to allow sensor readings to update


print("Facing backwards")
rc.turn("clockwise", 0.5, 6.4)
print("DONE!")
move_stop()
rc.turn("clockwise", 0.5, 9.25)
move_stop()
rc.turn("clockwise", 0.5, 6.1)