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

#OSC configuration
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

client.send_message("/x", 10)
client.send_message("/y", -10)
client.send_message("/z", 0)

def pos():
    l = "/?"  #ask for machine position
    print('Sending: ' + l)
    s.write(l.encode() + '\n'.encode()) # Send g-code block to grbl
    
    
    
def decode_response():
    
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print("message decoded: " + grbl_out)
    
    if(len(grbl_out)> 1):
        if(grbl_out.find("<Run|WPos") != -1):
            #print("pos message")
            # s = "<Run|WPos:-0.00,-303.840,-10.498|Bf:0,111|FS:1800,0>"
            x = grbl_out.split("|")
            print(x)
            y = x[1]
            z = y.split(":")
            pos = z[1]
            coords = pos.split(",")
            print(coords)
            #client.send_message("/x", float(coords[0]))
            #client.send_message("/y", float(coords[1]))
            #client.send_message("/z", float(coords[2]))
            #print(' : ' + coords)

def send_OSC():
    client.send_message("/x", float(abs_x))
    client.send_message("/y", float(abs_y))
    

def configure_plotter():
    print("configuring plotter")

    #movement parameters: RELATIVE COORDINATES and milimiters
    l = "G90 G21"
    print('Sending: ' + l)
    s.write(l.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print(' : ' + grbl_out.strip())
    
    
    #plektrum up to the middle, without electricity it is all down
    comm = "G01 " + "F400"
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print(' : ' + grbl_out.strip())
    
    #PUT THE PLEKTRUM SLIGHTLY DOWN 
    comm = "G01 " + "Z0.5"
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print(' : ' + grbl_out.strip())
    
    #try one time to put it down
    time.sleep(0.5)
    comm = "G01 " + "Z" + str(abs_z)
    #print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    time.sleep(0.5)  #back to movement position
    comm = "G01 " + "Z0.5"
    #print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    time.sleep(0.5)
    
  
        
def strum():
    
    global abs_x
    global abs_y
    global abs_z
    
    
    #plektrum down
    comm = "G01 " + "F400"
    #print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    decode_response()
    #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print(' : ' + grbl_out.strip())
    
    comm = "G01 " + "Z" + abs_z
    #print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    decode_response()
    #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print(' : ' + grbl_out.strip())
    
    
    #make the strumming movement
    
    for x in range(random.randint(11,21)):  #hardcoded by now, a random.randint() would be next
        
        #set strumming feed rate for whole strumming part
        strum_feed = str(random.randint(5000,8000))
        comm = "G01 " + "F" + strum_feed
        #print('Sending: '+ comm)
        s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
        decode_response()
        #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
        #print(' : ' + grbl_out.strip())
        
        strum_length = random.randint(20,50)
        
        #strumming movement 
        abs_y = str(int(abs_y) - strum_length) #go right
        mov = "G01 " + "Y" + abs_y
        #print('Sending: ' + mov)
        s.write(mov.encode() + '\n'.encode()) # Send g-code block to grbl
        decode_response()
        #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
        #print(' : ' + grbl_out.strip())
        
        time.sleep(round(random.uniform(0.11, 0.88), 2))
        
        abs_y = str(int(abs_y) + strum_length) #go left
        mov = "G01 " + "Y" + abs_y
        #print('Sending: ' + mov)
        s.write(mov.encode() + '\n'.encode()) # Send g-code block to grbl
        decode_response()
        #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
        #print(' : ' + grbl_out.strip())
        
        #time.sleep(0.5)
    
    #plektrum up
    comm = "G01 " + "F400"
    #print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    decode_response()
    #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print(' : ' + grbl_out.strip())
    
    comm = "G01 " + "Z0.5"
    #print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    decode_response()
    #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print(' : ' + grbl_out.strip())
    time.sleep(3)

def move():
    
    global abs_x
    global abs_y
    
    
    #movement in absolute mode
    for x in range(random.randint(4,7)):  #5,15
        
        #set feed rate
        feed = str(random.randint(5000,8000))
        comm = "G01 " + "F" + feed
        print('Sending: '+ comm)
        s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
        decode_response()
        
        #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
        #print(' : ' + grbl_out.strip())
    
        #movement to another position
        abs_x = str(random.randint(10,270))
        abs_y = str((-1)*random.randint(60,280))
        mov = "G01 " + "X" + abs_x + " " + "Y" + abs_y
        print('Sending: ' + mov)
        s.write(mov.encode() + '\n'.encode()) # Send g-code block to grbl
        #time.sleep(1);
        decode_response()
        #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
        #print(' : ' + grbl_out.strip())
        
        send_OSC()
        
        time.sleep(3); #WAIT 3 SECONDS TO STRUM
        
        strum()
        #time.sleep(3);
        

    
#------------PROGRAM ------
        
abs_x = str(0)
abs_y = str(0)
abs_z = str(1.4)


# Open grbl serial port of the machine
s = serial.Serial('/dev/tty.usbmodem201912341',115200)
  
# Wake up grbl
s.write("\r\n\r\n".encode())
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input
time.sleep(0.5)

#init plotter movement parameters
configure_plotter()



#----------MOVEMENTS

move()



print("end generative")

pos()

#HOME THE MACHINE AFTER ACTION
#set feed rate
comm = "G01 " + "F1000"
print('Sending: '+ comm)
s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
#grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
#print(' : ' + grbl_out.strip())

#movement
abs_x = str(10)
abs_y = str(-10)
mov = "G01 " + "X" + abs_x + " " + "Y" + abs_y
print('Sending: ' + mov)
s.write(mov.encode() + '\n'.encode()) # Send g-code block to grbl
#grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
#print(' : ' + grbl_out.strip())
client.send_message("/x", 10)
client.send_message("/y", -10)

# Wait here until grbl is finished to close serial port and file.
#raw_input("  Press <Enter> to exit and disable grbl.")

time.sleep(15) 
# Close file and serial port
#f.close()

s.close()

print("end program")
