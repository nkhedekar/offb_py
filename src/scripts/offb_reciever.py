#!/usr/bin/env python

import rospy
import numpy
from geometry_msgs.msg import *
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import SetMode
from mavros_msgs.msg import State

current_state = State()
pose = PoseStamped()

rospy.init_node('offb_node', anonymous=True)
rate = rospy.Rate(100)

def state_cb(msg):
	global current_state
	current_state = msg
	#print "callback state"

#def waypoint_reciever():
#	rospy.Subscriber("wayponits", PoseStamped, cb_move)

"""
def cb_move(msg):
	#print "subscribed"
	#pose = msg
	local_pos_pub.publish(msg)
	print msg
	rate.sleep()
"""

def cb_move(msg):
	global pose
	point = msg
	#local_pos_pub.publish(point)
	local_vel_pub.publish(vel)
	pose = point
	#rate.sleep()
	#print pose

def pose_cb(msg):
	global pose
	#print "in pose_cb"
	desired_pose = numpy.array((pose.pose.position.x, pose.pose.position.y, pose.pose.position.z))
	current_pose = numpy.array((msg.pose.position.x, msg.pose.position.y, msg.pose.position.z))
	print numpy.linalg.norm(desired_pose - current_pose)
	print desired_pose[0] - current_pose[0], desired_pose[1] - current_pose[1] 


if __name__=="__main__":
	#global pose
	global current_state
		
	rospy.Subscriber("mavros/state", State, state_cb)
	local_vel_pub = rospy.Publisher('mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
	

	local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
	print("Publisher and Subscriber Created")

	arming_client = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
	set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode)
	print("Clients Created")

	
	while(not current_state.connected):
		#print(current_state.connected)
		rate.sleep()
	
	
	#set position here
	pose.pose.position.x = 0
	pose.pose.position.y = 0
	pose.pose.position.z = 2
	
	vel = TwistStamped()
	vel.twist.linear.x = 200
	vel.twist.linear.y = 200
	vel.twist.linear.z = 200
		

	for i in range(100):
		local_pos_pub.publish(pose)
		#print current_state
		#print "check mission recieved"
		rate.sleep()
		
	print("Creating Objects for services")
	offb_set_mode = SetMode()
	offb_set_mode.custom_mode = "OFFBOARD"
	arm_cmd = CommandBool()
	arm_cmd.value = True
	
	last_request = rospy.Time.now()
	
	rospy.Subscriber("waypoints", PoseStamped, cb_move)
	rospy.Subscriber("/mavros/local_position/pose", PoseStamped, pose_cb)
	
	while not rospy.is_shutdown():
		#print(current_state)
		if(current_state.mode != "OFFBOARD" and (rospy.Time.now() - last_request > rospy.Duration(5.0))):
			resp1 = set_mode_client(0,offb_set_mode.custom_mode)
			if resp1.mode_sent:
				print ("Offboard enabled")
			last_request = rospy.Time.now()
		elif (not current_state.armed and (rospy.Time.now() - last_request > rospy.Duration(5.0))):
			arm_client_1 = arming_client(arm_cmd.value)
			if arm_client_1.success:
				print("Vehicle armed")
			last_request = rospy.Time.now()
			
		
		#print("subscribed in loop")
		#print(current_state)
		#rospy.spin()
		
		#local_pos_pub.publish(pose)
		#rate.sleep()

