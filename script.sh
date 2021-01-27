sudo ip link set can0 type can bitrate 125000
sudo ip link set can0 up 
roslaunch can_send test.launch 

