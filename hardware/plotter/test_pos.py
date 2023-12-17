#!/usr/bin/env python
"""\
Simple generative g-code streaming script for grbl Satoshiii

Machine should be switched on at 0,0,0 coordinate as we use
absolute coordinate movements with G90
"""
 
import serial
import time
import random

import argparse

from pythonosc import udp_client

abs_x = str(0)
abs_y = str(0)
abs_z = str(1.5)

    

def configure_plotter():
    print("configuring plotter")

    #movement parameters: ABSOLUTE COORDINATES and milimiters
    l = "G90 G21"
    print('Sending: ' + l)
    s.write(l.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())

    #l = "F1600"  #an inial feedrate just in case it is missing
    #print('Sending: ' + l)
    #s.write(l.encode() + '\n'.encode()) # Send g-code block to grbl
    #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print(' : ' + grbl_out.strip())
    
    
    #plektrum down
    comm = "G01 " + "F400"
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    comm = "G01 " + "Z" + str(abs_z)
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    time.sleep(1);
    #plektrum up
    comm = "G01 " + "F400"
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    comm = "G01 " + "Z" + "-"+ str(abs_z)
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    time.sleep(0.5)
  
        
def strum():
    
    global abs_x
    global abs_y
    global abs_z
    
    #plektrum down
    comm = "G01 " + "F400"
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    comm = "G01 " + "Z" + abs_z
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    
    #make the strumming movement
    
    for x in range(1):  #hardcoded by now, a random.randint() would be next
        
        #set strumming feed rate for whole strumming part
        strum_feed = str(random.randint(5000,8000))
        comm = "G01 " + "F" + strum_feed
        print('Sending: '+ comm)
        s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
        grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
        print(' : ' + grbl_out.strip())
        
        strum_length = random.randint(10,40)
        
        #strumming movement 
        abs_y = str(int(abs_y) - strum_length) #go right
        mov = "G01 " + "Y" + abs_y
        print('Sending: ' + mov)
        s.write(mov.encode() + '\n'.encode()) # Send g-code block to grbl
        grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
        print(' : ' + grbl_out.strip())
    
        abs_y = str(int(abs_y) + strum_length) #go left
        mov = "G01 " + "Y" + abs_y
        print('Sending: ' + mov)
        s.write(mov.encode() + '\n'.encode()) # Send g-code block to grbl
        grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
        print(' : ' + grbl_out.strip())
    
    #plektrum up
    comm = "G01 " + "F400"
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    comm = "G01 " + "Z" + "-"+ abs_z
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    time.sleep(0.5)

def move():
    
    global abs_x
    global abs_y
    
    #movement in absolute mode
    for x in range(1):
        
        #set feed rate
        feed = str(random.randint(5000,8000))
        comm = "G01 " + "F" + feed
        print('Sending: '+ comm)
        s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
        grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
        print(' : ' + grbl_out.strip())
    
        #movement to another position
        abs_x = str(random.randint(10,270))
        abs_y = str((-1)*random.randint(60,320))
        client.send_message("/x", int(abs_x))
        client.send_message("/y", int(abs_y))
        mov = "G01 " + "X" + abs_x + " " + "Y" + abs_y
        print('Sending: ' + mov)
        s.write(mov.encode() + '\n'.encode()) # Send g-code block to grbl
        grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
        print(' : ' + grbl_out.strip())
    
        strum()
        
        time.sleep(0.5)
    
#------------PROGRAM ------
# Open grbl serial port of the machine
s = serial.Serial('/dev/tty.usbmodem201912341',115200)
  
# Wake up grbl
s.write("\r\n\r\n".encode())
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input
time.sleep(0.5)

#init plotter movement parameters
configure_plotter()

l = "?"
print('Sending: ' + l)
s.write(l.encode() + '\n'.encode()) # Send g-code block to grbl
grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
print(' : ' + grbl_out.strip())

#configure OSC
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

client.send_message("/x", 0)
client.send_message("/y", 0)

#----------MOVEMENTS

#move()


print("end generative")

#HOME THE MACHINE AFTER ACTION
"""\
#set feed rate
comm = "G01 " + "F1000"
print('Sending: '+ comm)
s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
print(' : ' + grbl_out.strip())
#movement
abs_x = str(10)
abs_y = str(10)
mov = "G01 " + "X" + abs_x + " " + "Y" + abs_y
print('Sending: ' + mov)
s.write(mov.encode() + '\n'.encode()) # Send g-code block to grbl
grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
print(' : ' + grbl_out.strip())

# Wait here until grbl is finished to close serial port and file.
#raw_input("  Press <Enter> to exit and disable grbl.")
"""

time.sleep(1) 
# Close file and serial port
#f.close()

s.close()

print("end program")

