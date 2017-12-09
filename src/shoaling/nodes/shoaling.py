#! /usr/bin/python

'''
This should run in any linux system using the command
    $ ./shoaling.py
If permission is denied, use
    $ chmod +x shoaling.py
Then try again.
'''

from numpy.random import randn # Because random.gauss doesn't quite cut it
from math import sqrt, sin, cos

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import time

N=1

#params
eta = 3.5847
sigma = 1.2667
speed = 0.1
T = 120 # seconds
dt = 0.01 # this is also the response latency so 10 ms

# intialize
#timeSteps=1:dt:T
timeSteps = [0] * int(T/dt)
counter = 0

NODE_NAME = 'iRobot_1'
TOPIC = 'cmd_vel'
if __name__ == "__main__":
    publisher = rospy.Publisher(TOPIC, Twist, queue_size = 1)
    rospy.init_node(NODE_NAME)

    pub = rospy.Publisher(NODE_NAME + '_position', Twist, queue_size=1)

    speed = rospy.get_param("~speed", 1.0)
    turn = rospy.get_param("~turn", 1.0)
    run = True
    forwardSpeed = speed/4
    print "Running"

    prevOrientation = 0
    prevOmega = randn(N,1) * 0.01
    for period in timeSteps:
        DW = randn() * sqrt(dt) * sigma
        omega = prevOmega * (1 - eta*dt) + DW
        o = prevOrientation + omega*dt
        twist = Twist()
        twist.linear.x = forwardSpeed
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0

        twist.angular.z = (o-prevOrientation)/0.01
        prevOrientation = o

        #publisher.publish(twist)
        pub.publish(twist)
        time.sleep(0.01)

    print "Exiting"

