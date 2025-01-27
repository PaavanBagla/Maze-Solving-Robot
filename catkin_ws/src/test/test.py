#! usr/bin/env python

from robot_control_class import RobotControl
import time

rc = RobotControl()
exit_flag = True
dist = rc.get_laser(360)

while dist > 1:
    dist = rc.get_laser(360)
    print("Distance from the front wall: ", dist)
    rc.move_straight()

rc.stop_robot()
print("Done!")

"""
def move_straight(self):

        # Initilize velocities
        self.cmd.linear.x = 0.5
        self.cmd.linear.y = 0
        self.cmd.linear.z = 0
        self.cmd.angular.x = 0
        self.cmd.angular.y = 0
        self.cmd.angular.z = 0

        # Publish the velocity
        self.publish_once_in_cmd_vel()

"""

# def move_stop():
#     global exit_flag
#     while True:
#         dist = rc.get_laser(360)
#         if dist == float('inf'):
#             left, right = get_readings()
#             print("Distance measured from left: ", left)
#             print("Distance measured from right: ", right)
#             if left == float('inf') and right == float('inf'):
#                 exit_flag = False
#                 rc.stop_robot()
#                 print("Escaped!")
#                 break
#             rc.move_straight()
#         elif dist <= 1:  # Increased threshold to 1.5 meters
#             rc.stop_robot()
#             break
#         else:
#             rc.move_straight()
#             print("Distance measured from front: ", dist)
#         time.sleep(0.1)  # Small delay to allow sensor readings to update

# def get_readings():
#     left_reading = rc.get_laser(719)
#     right_reading = rc.get_laser(0)
#     return left_reading, right_reading

# def turn():
#     left, right = get_readings()
#     if (right > 1):
#         print("Turning to the right")
#         rc.rotate(-90)
#     else:
#         print("Turning to the left")
#         rc.rotate(90)

# while exit_flag:
#     while True:
#         move_stop()
#         if exit_flag == False:
#             break
#         turn()