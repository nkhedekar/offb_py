# offb_py
Python implementation of the offboard example at https://dev.px4.io/en/ros/mavros_offboard.html

## Tutorial 
```
cd catkin_ws/src
git clone https://github.com/nkhedekar/offb_py.git
cd ..
catkin_make
source devel/setup.bash
```

Run MAVROS and Gazebo in two terminals 
```
roslaunch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14557"
roslaunch px4 posix_sitl.launch
```

Run the node (in the sourced terminal)
```
rosrun offb_py offb.py
```


