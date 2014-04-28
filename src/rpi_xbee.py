#!/usr/bin/env python

import time
import picamera
import socket

#########################
#########################
## Assignment of GPIOs ##
rled_pin = '17'
bled_pin = '27'
outlet0_pin = '9'
outlet1_pin = '10'
#prox0_pin = '22'
sw_pin = '4'        #motion fed through switch

####################
# rled_pin, GPIO17 #
####################
#Ensure resource availability
try:
    f= open('/sys/class/gpio/unexport','w')
    f.write(rled_pin)
    f.close()
except IOError as e:
    lol = 0

#Export rled_pin
f= open('/sys/class/gpio/export','w')
f.write(rled_pin)
f.close()

#Direction > OUTPUT for rled_pin
path = '/sys/class/gpio/gpio' + rled_pin + '/direction'
f= open(path,'w')
f.write('out')
f.close()

####################
# bled_pin, GPIO27 #
####################
#Ensure resource availability
try:
    f= open('/sys/class/gpio/unexport','w')
    f.write(bled_pin)
    f.close()
except IOError as e:
    lol = 0

#Export bled_pin
f= open('/sys/class/gpio/export','w')
f.write(bled_pin)
f.close()

#Direction > OUTPUT for bled_pin
path = '/sys/class/gpio/gpio' + bled_pin + '/direction'
f= open(path,'w')
f.write('out')
f.close()

#####################
# outlet0_pin, GPIO9 #
#####################
#Ensure resource availability
try:
    f= open('/sys/class/gpio/unexport','w')
    f.write(outlet0_pin)
    f.close()
except IOError as e:
    lol = 0

#Export outlet0_pin
f= open('/sys/class/gpio/export','w')
f.write(outlet0_pin)
f.close()

#Direction > OUTPUT for outlet0_pin
path = '/sys/class/gpio/gpio' + outlet0_pin + '/direction'
f= open(path,'w')
f.write('out')
f.close()

#####################
# outlet1_pin, GPI10 #
#####################
#Ensure resource availability
try:
    f= open('/sys/class/gpio/unexport','w')
    f.write(outlet1_pin)
    f.close()
except IOError as e:
    lol = 0

#Export outlet1_pin
f= open('/sys/class/gpio/export','w')
f.write(outlet1_pin)
f.close()

#Direction > OUTPUT for outlet1_pin
path = '/sys/class/gpio/gpio' + outlet1_pin + '/direction'
f= open(path,'w')
f.write('out')
f.close()

'''
#####################
# prox0_pin, GPIO22 #
#####################
#Ensure resource availability
try:
    f= open('/sys/class/gpio/unexport','w')
    f.write(prox0_pin)
    f.close()
except IOError as e:
    lol = 0

#Export prox0_pin
f= open('/sys/class/gpio/export','w')
f.write(prox0_pin)
f.close()

#Direction > INPUT for prox0_pin
path = '/sys/class/gpio/gpio' + prox0_pin + '/direction'
f= open(path,'w')
f.write('in')
f.close()
'''

#####################
# sw_pin, GPIO4 #
#####################
#Ensure resource availability
try:
    f= open('/sys/class/gpio/unexport','w')
    f.write(sw_pin)
    f.close()
except IOError as e:
    lol = 0

#Export sw_pin
f= open('/sys/class/gpio/export','w')
f.write(sw_pin)
f.close()

#Direction > INPUT for sw_pin
path = '/sys/class/gpio/gpio' + sw_pin + '/direction'
f= open(path,'w')
f.write('in')
f.close()

############################
# Value paths for all pins #
rled_path = '/sys/class/gpio/gpio' + rled_pin + '/value'
bled_path = '/sys/class/gpio/gpio' + bled_pin + '/value'
outlet0_path = '/sys/class/gpio/gpio' + outlet0_pin + '/value'
outlet1_path = '/sys/class/gpio/gpio' + outlet1_pin + '/value'
#prox0_path = '/sys/class/gpio/gpio' + prox0_pin + '/value'
sw_path = '/sys/class/gpio/gpio' + sw_pin + '/value'
############################

#########################
#########################
i=0;
stop = 0
#everything initially off
outlet0_state = '0'
outlet1_state = '0'
cam_state = '0'
outlet0_motion = 0  #timer once activated counts down to 1
outlet1_motion = 0  #initially deactivated
cam_motion = 0
motion_count = 20
file_number = 1

while(stop != 1)

    #aquire values from cloud; convert state bits to strings; motion bits are ints
    # name_cld = name_cld[0]            name_cld[1]
    #            State: off(0)/on(1)    Motion:no(0)/yes(1)
    # 00:off    10:on   01:motion   11:undefined

    outlet0_cld_s = str(outlet0_cld[0]) #state bit -- string
    outlet0_cld_m = outlet0_cld[1]      #motion bit -- int
    outlet1_cld_s = str(outlet1_cld[0])
    outlet1_cld_m = outlet1_cld[1]
    cam_cld_s = str(cam_cld[0])
    cam_cld_m = cam_cld[1]
    
    ########################
    # outlet0 cloud update #
    if outlet0_cld_m == 0
        outlet0_motion = 0
        
        # Update outlet0 state
        if outlet0_cld_s != outlet0_state
            outlet0_state = outlet0_cld_s
            f= open(outlet0_path,'w')
            f.write(outlet0_state)
            f.close
        else:
            pass
        
    #motion prev disabled, now enabled via update
    elif outlet0_motion == 0    #&& outlet0_cld_m == 1
        outlet0_motion = 1
        
    else:
        pass #continue motion countdown;
             #outlet0_cld_m == 1 && outlet_motion != 0 -> countdown active
    ########################

    ########################
    # outlet1 cloud update #
    if outlet1_cld_m == 0
        outlet1_motion = 0
        
        # Update outlet1 state
        if outlet1_cld_s != outlet1_state
            outlet1_state = outlet1_cld_s
            f= open(outlet1_path,'w')
            f.write(outlet1_state)
            f.close
        else:
            pass
        
    #motion prev disabled, now enabled via update    
    elif outlet1_motion == 0
        outlet1_motion = 1
        
    else:
        pass #continue motion countdown       
    ########################

    ####################
    # Cam cloud update #
    ####################

    ########################
    # Video motion storage #
    if cam_cld_m == 1
        cam_motion = 1

        with picamera.PiCamera() as cam:
            cam.resolution = (640, 480)
            cam.start_recording('motion_record' + str(file_number) + '.h264')
            cam.wait_recording(5)
            cam.stop_recording()

            file_number += 1

    
    elif cam_cld_m == 0
        cam_motion = 0

        #####################################
        # Cloud Connection for Video Stream #
        if cam_cld_s == '1'
            cam_state = '1'
            cam_time = 10
            cloud_server = ''
            rpi_socket = socket.socket()
            rpi_socket.connect((cloud_server, 8000))
            link = rpi_socket.makefile('wb')

            try:
                with picamera.PiCamera() as cam:
                    cam.resolution - (640,480)
                    cam.start_recording(link, format='h264')
                    cam.wait_recording(cam_time)
                    cam.stop_recording()

            finally:
                link.close()
                rpi_socket.close()
                cam_state = '0'    #after timed recording camera will turn off
                
                #account for time of camera w/respect to motion delay
                if outlet0_motion > 0
                    outlet0_motion = 1    #cam_time will have consumed any motion delay
                else:
                    pass
                if outlet1_motion > 0
                    outlet1_motion = 1
                else:
                    pass
        else:
            pass
        #####################################
    else:
        print('error in cam_cld_s = ' + cam_cld_s)
    ################   

    ################
    # Motion check #
    f= open(sw_path,'r')    #motion sensor connected to switch
    sw_val = f.read(1)
    f.close()

    #No motion detected
    if sw_val == '1'
    
        if outlet0_motion > 1
            outlet0_motion -= 1    #decrementing motion delay
        else:
            pass
        if outlet1_motion > 1
            outlet1_motion -= 1
        else:
            pass

    #Motion detected
    elif sw_val == '0'

        if outlet0_motion > 0
            outlet0_motion = motion_count    #reset count if motion detected and enabled
        else:
            pass
        if outlet1_motion > 0
            outlet1_motion = motion_count
        else:
            pass

    else:
        print('error in motion, sw_val = ' + sw_val)
    ################    

    time.sleep(0.25)


'''
###################
# Motion LED test #
while(i < 40):
    
    f= open(sw_path,'r')
    sw_val = f.read(1)	#using 1 avoids reading "\n" char
    f.close()
    print('sw_val = ' + sw_val)

    #Motion is active low
    if sw_val == '0':
        f= open(bled_path,'w')
        f.write('1')
        f.close()

    elif sw_val == '1':
	f= open(bled_path,'w')
        f.write('0')
        f.close()

    else:
	print('error: neither 1 or 0')

    time.sleep(0.25)
    i+=1
    print('i = ' + str(i))
#################

###################
# Motion outlet0 test #
while(i < 40):
    
    f= open(sw_path,'r')
    sw_val = f.read(1)	#using 1 avoids reading "\n" char
    f.close()
    print('sw_val = ' + sw_val)

    #Motion is active low
    if sw_val == '0':
        f= open(outlet0_path,'w')
        f.write('1')
        f.close()

    elif sw_val == '1':
	f= open(outlet0_path,'w')
        f.write('0')
        f.close()

    else:
	print('error: neither 1 or 0')

    time.sleep(0.25)
    i+=1
    print('i = ' + str(i))
#################

#Debug code
while(i < 10):
    
    f= open(sw_path,'r')
    sw_val = f.read(1)	#using 1 avoids reading "\n" char
    f.close()
    print('sw_val = ' + sw_val)

    if sw_val == '0':
        f= open(rled_path,'w')
        f.write('0')
        f.close()

    elif sw_val == '1':
	f= open(rled_path,'w')
        f.write('1')
        f.close()

    else:
	print('neither 1 or 0')

    time.sleep(0.5)
    i+=1
    print('i = ' + str(i))
'''
    
#################
# Unexport Pins #
f= open('/sys/class/gpio/unexport','w')
f.write(rled_pin)
f.close()
f= open('/sys/class/gpio/unexport','w')
f.write(bled_pin)
f.close()
f= open('/sys/class/gpio/unexport','w')
f.write(outlet0_pin)
f.close()
f= open('/sys/class/gpio/unexport','w')
f.write(outlet1_pin)
f.close()
#f= open('/sys/class/gpio/unexport','w')
#f.write(prox0_pin)
#f.close()
f= open('/sys/class/gpio/unexport','w')
f.write(sw_pin)
f.close()
print('Unexported all pins')
#################
