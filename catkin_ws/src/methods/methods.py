#! usr/bin/env python

from robot_control_class import RobotControl

rc = RobotControl()
methods = dir(rc)
print(methods)
help(rc.turn)