#!/usr/bin/env python

import rospy
import random
from std_msgs.msg import *

pub = rospy.Publisher('chatter', Int16, queue_size=10)
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(10)


def talker():
	while not rospy.is_shutdown():
		a = random.randint(5,10)
		pub.publish(a)
		print (a)
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass