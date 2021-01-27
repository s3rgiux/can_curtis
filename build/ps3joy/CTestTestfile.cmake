# CMake generated Testfile for 
# Source directory: /home/jetson/catkin_ws/src/joystick_drivers/ps3joy
# Build directory: /home/jetson/catkin_ws/build/ps3joy
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_ps3joy_roslint_package "/home/jetson/catkin_ws/build/ps3joy/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/jetson/catkin_ws/build/ps3joy/test_results/ps3joy/roslint-ps3joy.xml" "--working-dir" "/home/jetson/catkin_ws/build/ps3joy" "--return-code" "/opt/ros/melodic/share/roslint/cmake/../../../lib/roslint/test_wrapper /home/jetson/catkin_ws/build/ps3joy/test_results/ps3joy/roslint-ps3joy.xml make roslint_ps3joy")
subdirs("gtest")
