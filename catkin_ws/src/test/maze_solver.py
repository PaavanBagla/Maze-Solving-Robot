import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import time

class WallFollower:
    # Initializing the node
    def __init__(self):
        rospy.init_node("wall_follower")

        # Subscribe to the LaserScan msgs
        self.scan_sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, self.scan_callback)

        # Publish the velocities: geometry msgs
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        self.cmd = Twist()
        self.rate = rospy.Rate(10)
        self.state = 'forward'  # Initial state
        self.turn_right_time = None  # Timer for turning right
        self.turn_left_time = None  # Timer for turning left

    def scan_callback(self, data):
        # Define regions based on laser scan data
        self.regions = {
            'front': min(data.ranges[340:360]),  # Front region
            'left': min(data.ranges[700:720]),   # Left region
            'right': min(data.ranges[0:20])      # Right region
        }
        rospy.loginfo("Regions: {}".format(self.regions))
        self.wall_following_logic()

    def wall_following_logic(self):
        linear_speed = 0.7
        angular_speed = 0.4

        front_distance = self.regions['front']
        left_distance = self.regions['left']
        right_distance = self.regions['right']

        if self.state == 'turn_right' and self.turn_right_time is not None:
            # Check if the turn right delay has passed
            if time.time() - self.turn_right_time > 1.5:  # 1.5 second delay
                self.state = 'forward'
                self.turn_right_time = None
            else:
                self.cmd.linear.x = 0
                self.cmd.angular.z = -angular_speed
                rospy.loginfo("Turning right")
                self.cmd_pub.publish(self.cmd)
                return

        # if self.state == 'turn_right':
        #     # Check if the turn right delay has passed
        #     if left_distance > 0.5:
        #         self.state = 'forward'
        #     else:
        #         self.cmd.linear.x = 0
        #         self.cmd.angular.z = -angular_speed
        #         rospy.loginfo("Turning right")
        #         self.cmd_pub.publish(self.cmd)
        #         return

        if self.state == 'turn_left' and self.turn_left_time is not None:
            # Check if the turn left delay has passed
            if time.time() - self.turn_left_time > 1.7:  # 1.7 second delay
                self.state = 'forward'
                self.turn_left_time = None
            else:
                self.cmd.linear.x = 0
                self.cmd.angular.z = angular_speed
                rospy.loginfo("Turning left")
                self.cmd_pub.publish(self.cmd)
                return

        # if self.state == 'turn_left':
        #     # Check if the turn left delay has passed
        #     if right_distance > 0.5:  # 1.6 second delay
        #         self.state = 'forward'
        #     else:
        #         self.cmd.linear.x = 0
        #         self.cmd.angular.z = angular_speed
        #         rospy.loginfo("Turning left")
        #         self.cmd_pub.publish(self.cmd)
        #         return

        if front_distance > 0.8:
            if left_distance < 1.5:
                self.state = 'forward'
            else:
                self.state = 'turn_left'
                self.turn_left_time = time.time()  # Start the turn left timer
        else:
            if left_distance < 1:
                self.state = 'turn_right'
                self.turn_right_time = time.time()  # Start the turn right timer
            else:
                self.state = 'turn_left'
                self.turn_left_time = time.time()  # Start the turn left timer

        if self.state == 'forward':
            if left_distance > 1.5:
                # Reduce speed for slight left turn
                self.cmd.linear.x = linear_speed / 6
                self.cmd.angular.z = 0.5
            else:
                self.cmd.linear.x = linear_speed
                self.cmd.angular.z = 0
            rospy.loginfo("Moving forward")
        elif self.state == 'turn_right':
            self.cmd.linear.x = 0
            self.cmd.angular.z = -angular_speed
            rospy.loginfo("Turning right")
        elif self.state == 'turn_left':
            self.cmd.linear.x = 0
            self.cmd.angular.z = angular_speed
            rospy.loginfo("Turning left")

        self.cmd_pub.publish(self.cmd)

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

if __name__ == '__main__':
    try:
        wall_follower = WallFollower()
        wall_follower.run()
    except rospy.ROSInterruptException:
        pass