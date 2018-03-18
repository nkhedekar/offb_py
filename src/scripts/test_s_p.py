#!/usr/bin/env python

import rospy
import random
from std_msgs.msg import *

rospy.init_node('s_and_p', anonymous=True)

def cb_pub(data):
	pub = rospy.Publisher('data_out', Int16, queue_size=10)
	pub.publish(data)

def listner():
	rospy.Subscriber('chatter', Int16, cb_pub)
	rospy.spin()

if __name__ == '__main__':
	listner()