#!/usr/bin/env python

import rospy
from geometry_msgs.msg import *
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import SetMode
from mavros_msgs.msg import State
import math
import time
import random
import tf
import tf2_ros

way_pub = rospy.Publisher('waypoints', PoseStamped, queue_size=1)
rospy.init_node('waypoint_pub', anonymous=True)
rate = rospy.Rate(100)

def talker():
	waypoint = PoseStamped()
	waypoint.pose.position.x = -10
	waypoint.pose.position.y = -10
	waypoint.pose.position.z = 7
	t = 0
	
	#time.sleep(10)
	while not rospy.is_shutdown():
		for i in range(-1000, 1000):
			print "cycle 1"
			waypoint.pose.position.y = -10
			waypoint.pose.position.x = (float(i))/100
			q1 = tf.transformations.quaternion_from_euler(0, 0, 0)
			waypoint.pose.orientation.x = q1[0]
			waypoint.pose.orientation.y = q1[1]
			waypoint.pose.orientation.z = q1[2]
			waypoint.pose.orientation.w = q1[3]
			way_pub.publish(waypoint)
			t += 0.05
			print waypoint
			rate.sleep()
		
		for i in range(-1000, 1000):
			print "cycle 2"
			waypoint.pose.position.x = 10
			waypoint.pose.position.y = (float(i))/100
			q1 = tf.transformations.quaternion_from_euler(0, 0, 0)
			waypoint.pose.orientation.x = q1[0]
			waypoint.pose.orientation.y = q1[1]
			waypoint.pose.orientation.z = q1[2]
			waypoint.pose.orientation.w = q1[3]
			way_pub.publish(waypoint)
			t += 0.05
			print waypoint
			rate.sleep()

		for i in range(-1000,1000):
			print "cycle 3"
			waypoint.pose.position.y = 10
			waypoint.pose.position.x = (float(-i))/100
			q1 = tf.transformations.quaternion_from_euler(0, 0, 0)
			waypoint.pose.orientation.x = q1[0]
			waypoint.pose.orientation.y = q1[1]
			waypoint.pose.orientation.z = q1[2]
			waypoint.pose.orientation.w = q1[3]
			way_pub.publish(waypoint)
			t += 0.05
			print waypoint
			rate.sleep()

		for i in range(-1000,1000):
			print "cycle 4"
			waypoint.pose.position.x = -10
			waypoint.pose.position.y = (float(-i))/100
			q1 = tf.transformations.quaternion_from_euler(0, 0, 0)
			waypoint.pose.orientation.x = q1[0]
			waypoint.pose.orientation.y = q1[1]
			waypoint.pose.orientation.z = q1[2]
			waypoint.pose.orientation.w = q1[3]
			way_pub.publish(waypoint)
			t += 0.05
			print waypoint
			rate.sleep()

		
		

if __name__ == '__main__':
	talker()
