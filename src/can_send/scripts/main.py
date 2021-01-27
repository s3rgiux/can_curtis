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

id_curtis1298=1574
id_curtis1222=1538
id_wago=1537
class SendCan:
    def __init__(self):
        print("Obstacle_extarctor")
        self.can_pub = rospy.Publisher('sent_messages', Frame, queue_size=1)
        self.sub = rospy.Subscriber('/j0/joy',Joy,self.callbackJoy)
        self.message = Frame()
        self.enabled_controller=False
        self.enabled_wago=False
        self.message.id=id_curtis1298#626
        self.message.dlc=8
        self.cont_wago=0
        
    def callbackJoy(self,joy):
        buttons=joy.buttons
        axes=joy.axes
        
        if axes[7]==1:
             if self.enabled_wago:
                 self.setup_for_wago()
                 self.cont_wago=self.cont_wago+1
                 if (self.cont_wago>=254):
                     self.cont_wago=254
                 temp_data=[47,0,98,01,self.cont_wago,0,0,0]#send to turn on lights 2F 00 62 01 number 00 00 00
                 self.message.data=temp_data

        if axes[7]==-1:
             if self.enabled_wago:
                 self.setup_for_wago()
                 self.cont_wago=self.cont_wago-1
                 if (self.cont_wago<=0):
                     self.cont_wago=0
                 temp_data=[47,0,98,01,self.cont_wago,0,0,0]#send to turn on lights 2F 00 62 01 number 00 00 00
                 self.message.data=temp_data
                 
        if buttons[2]:#circle
             
             #temp_data=[34,62,48,00,0,0,0,0]#disable interlock 22 3E 30 00 00 00 00 00
             self.setup_for_c1298()
             temp_data=[34,62,48,00,2,0,0,0]#enable interlock  22 3E 30 00 02 00 00 00
             self.message.data=temp_data
             print('enable interlock')
             self.enabled_controller=True
             self.can_pub.publish(self.message)

        if buttons[1]:#cross
             #self.message.id=1574#626
             #self.message.dlc=8
             self.setup_for_c1298()
             temp_data=[34,62,48,00,0,0,0,0]#disable interlock 22 3E 30 00 00 00 00 00
             #temp_data=[34,62,48,00,2,0,0,0]#enable interlock  22 3E 30 00 02 00 00 00
             self.message.data=temp_data
             print('disable interlock')
             self.enabled_controller=False
             self.can_pub.publish(self.message)
        
        if buttons[0]:#square
             self.setup_for_enable_wago()
             temp_data=[1,1,0,0,0,0,0,0]#enable
             self.message.data=temp_data
             print('enable wago')
             self.enabled_wago=True
             self.can_pub.publish(self.message)

        if buttons[3]:#triangle
             self.setup_for_enable_wago()
             temp_data=[2,1,0,0,0,0,0,0]#disable 
             self.message.data=temp_data
             print('enable wago')
             self.enabled_wago=False
             self.can_pub.publish(self.message)

        if self.enabled_controller==True:
             tmp=axes[1]
             self.setup_for_c1298()
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
       
    def setup_for_c1298(self):
        self.message.id=id_curtis1298#626
        self.message.dlc=8

    def setup_for_enable_wago(self):
        self.message.id=0#0
        self.message.dlc=2

    def setup_for_c1222(self):
        self.message.id=id_curtis1222#602
        self.message.dlc=8

    def setup_for_wago(self):
        self.message.id=id_wago#601
        self.message.dlc=5
        
    
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
