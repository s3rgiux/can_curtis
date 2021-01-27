#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import sys,time
from math import sqrt, cos, sin
import rospy
#import tf,tf2_ros
import numpy as np
from time import sleep
from geometry_msgs.msg import Twist, Pose, TransformStamped,Quaternion
from sensor_msgs.msg import Imu, JointState
from sensor_msgs.msg import Joy

#from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Float32
from std_msgs.msg import *
from geometry_msgs.msg import Point, Vector3, PoseWithCovarianceStamped

from can_send.msg import Frame

import commands as cmd
import struct
import time
import rosparam
import atexit


baud = 1000000

SLEEP_TIME = 0.9
#200mm diameter

id1=1574
class SendCan:
    def __init__(self):
        print("Obstacle_extarctor")
        self.can_pub = rospy.Publisher('sent_messages', Frame, queue_size=1)
        self.sub = rospy.Subscriber('/j0/joy',Joy,self.callbackJoy)
        self.message = Frame()
        self.enabled_controller=False
        self.message.id=id1#626
        self.message.dlc=8
        
    def callbackJoy(self,joy):
        buttons=joy.buttons
        axes=joy.axes
        if buttons[2]:#circle
             
             #temp_data=[34,62,48,00,0,0,0,0]#disable interlock 22 3E 30 00 00 00 00 00
             temp_data=[34,62,48,00,2,0,0,0]#enable interlock  22 3E 30 00 02 00 00 00
             self.message.data=temp_data
             print('enable interlock')
             self.enabled_controller=True
             self.can_pub.publish(self.message)

        if buttons[1]:#cross
             #self.message.id=1574#626
             #self.message.dlc=8
             temp_data=[34,62,48,00,0,0,0,0]#disable interlock 22 3E 30 00 00 00 00 00
             #temp_data=[34,62,48,00,2,0,0,0]#enable interlock  22 3E 30 00 02 00 00 00
             self.message.data=temp_data
             print('disable interlock')
             self.enabled_controller=False
             self.can_pub.publish(self.message)

        if self.enabled_controller==True:
             tmp=axes[1]
             ##self.message.id=1574#626
             #self.message.dlc=8
             if tmp<=0.05 and tmp>=-0.05 :
                 tmp=0
             var=int(tmp*127)
             nv=np.uint8(var)
             print(var)
             temp_data=[34,24,50,00,00,nv,0,0]#disable interlock 22 3E 30 00 00 00 00 00
             self.message.data=temp_data
             self.can_pub.publish(self.message)               

        #elif self.enabled_controller==False:    
       
        
    def pub_data(self):
        #try:
        #self.message.id=1574#626
        #self.message.dlc=8
        temp_data=[34,62,48,00,0,0,0,0]#disable interlock 22 3E 30 00 00 00 00 00
        temp_data=[34,62,48,00,2,0,0,0]#enable interlock  22 3E 30 00 02 00 00 00
        self.message.data=temp_data
        self.can_pub.publish(self.message)
        #except:
        #    import traceback
        #    traceback.print_exc()

    def obstacles_callback(self, data):
        for x in data.circles:
            if x.center.x<-0.3 and x.center.x>-1.8 and x.center.y<.5 and x.center.y>-0.5: 
                print("#########")
                #circles = data.circles
                #print(circles)
                print(x)
                print("#########")
    
    

    def shutdown(self):
        rospy.sleep(1)
        

def send_can_main():
    rospy.init_node('send_can', anonymous = True)
    send_obj = SendCan()

    while not rospy.is_shutdown():
        #send_obj.pub_data()
        sleep(SLEEP_TIME)

if __name__=='__main__':
    send_can_main()
