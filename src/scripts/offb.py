#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import SetMode
from mavros_msgs.msg import State

current_state = State()

def state_cb(msg):
	global current_state
	current_state = msg

if __name__=="__main__":
	rospy.init_node('offb_node', anonymous=True)	
	rospy.Subscriber("mavros/state", State, state_cb)
	local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
	print("Pub and Sub done")
	arming_client = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
	set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode)
	print("clients ready")
	rate = rospy.Rate(20)
	while(not current_state.connected):
		print(current_state.connected)
		rate.sleep()
	
	print("creating pose")
	pose = PoseStamped()
	#set position here
	pose.pose.position.x = 1
	pose.pose.position.y = 1
	pose.pose.position.z = 2
	
	for i in range(100):
		local_pos_pub.publish(pose)
		rate.sleep()
	print("setting variable")
	offb_set_mode = SetMode()
	offb_set_mode.custom_mode = "OFFBOARD"
	arm_cmd = CommandBool()
	arm_cmd.value = True
	
	last_request = rospy.Time.now()
	
	while not rospy.is_shutdown():
		print(current_state)
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
			
		local_pos_pub.publish(pose)
		rate.sleep()
	
