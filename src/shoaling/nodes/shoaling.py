#! /usr/bin/python

'''
This is a direct translation of the matplot version that plots a trajectory
with some slight modifications for movement in ROS. It can be optimized
to run faster and use less memory by generating the new orientation every
iteration and only keeping track of the current and previous orientations.
This version runs for 2 minutes, 120 seconds, for testing purposes
but it can be modified to run perpetually by changing the inner for loop
to a while loop.

This should run in any linux system using the command
    $ ./Shoaling2.py
If permission is denied, use
    $ chmod +x Shoaling2.py
Then try again.
'''

from numpy.random import randn # Because random.gauss doesn't quite cut it
from math import sqrt, sin, cos

import rospy
from geometry_msgs.msg import Twist
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
timeSteps = []
counter = 0
while counter < T:
    timeSteps.append(0)
    counter += dt

# # # position
# # r=zeros(numel(timeSteps))+ 1i*zeros(numel(timeSteps));
# # r(1)=0.05*rand().*exp(1i*(-pi+2*pi*rand()));
# x = zeros(1,numel(timeSteps));
# y = zeros(1,numel(timeSteps));
x = [0] * len(timeSteps)
y = [0] * len(timeSteps)


# orientation
orientation = [0] * len(timeSteps)
orientation[0] = randn() * 2

omega = [0] * len(timeSteps)
omega[0] = randn(N,1) * 0.01;

for k in range(len(timeSteps)-1):
    DW = randn() * sqrt(dt) * sigma;
    omega[k+1] = omega[k]*(1 - eta*dt) + DW;
    orientation[k+1] = orientation[k] + omega[k+1]*dt
    #         r(k+1) = r(k) + speed*exp(1i*orientation(k+1))*dt;#polar coordinate
    ##in cartesian coordinate you have x and y below below
    x[k+1] = x[k] + speed * cos(orientation[k+1]) * dt;
    y[k+1] = y[k] + speed * sin(orientation[k+1]) * dt;


#TOPIC = '/turtle1/cmd_vel'
TOPIC = 'cmd_vel'
if __name__ == "__main__":
    publisher = rospy.Publisher(TOPIC, Twist, queue_size = 1)
    rospy.init_node('test_node')

    speed = rospy.get_param("~speed", 1.0)
    turn = rospy.get_param("~turn", 1.0)
    run = True
    forwardSpeed = speed/8
    print "Running"

    prev = orientation[0]
    for o in orientation:
        twist = Twist()
        twist.linear.x = forwardSpeed
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0

        twist.angular.z = (o-prev)/0.01
        prev = o

        publisher.publish(twist)
        time.sleep(0.01)

    print "Shoaing ended"

