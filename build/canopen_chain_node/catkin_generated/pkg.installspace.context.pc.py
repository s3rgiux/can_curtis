# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include;/usr/include".split(';') if "${prefix}/include;/usr/include" != "" else []
PROJECT_CATKIN_DEPENDS = "canopen_master;diagnostic_updater;message_runtime;pluginlib;rosconsole_bridge;roscpp;socketcan_interface;std_srvs".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lcanopen_ros_chain;/usr/lib/aarch64-linux-gnu/libboost_filesystem.so;/usr/lib/aarch64-linux-gnu/libboost_system.so".split(';') if "-lcanopen_ros_chain;/usr/lib/aarch64-linux-gnu/libboost_filesystem.so;/usr/lib/aarch64-linux-gnu/libboost_system.so" != "" else []
PROJECT_NAME = "canopen_chain_node"
PROJECT_SPACE_DIR = "/home/jetson/catkin_ws/install"
PROJECT_VERSION = "0.8.4"
