#!/usr/bin/env python
"""\
Simple generative g-code streaming script for grbl Satoshiii

Machine should be switched on at 0,0,0 coordinate as we use
absolute coordinate movements with G90
"""
 
import serial
import time
import random

    

def calibrate_z_plotter():
    print("configuring plotter")

    #movement parameters: ABSOLUTE COORDINATES and milimiters
    l = "G90 G21"
    print('Sending: ' + l)
    s.write(l.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    
    #plektrum up to the middle, without electricity it is all down
    comm = "G01 " + "F400"
    print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    
    #down the pen 3mm to the middle of the Z axis, it is still floating
    comm = "G01 " + "Z0.5"# + str(abs_z)
    #print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    time.sleep(2)
    comm = "G01 " + "Z1.6"# + str(abs_z)
    #print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    time.sleep(2)
    comm = "G01 " + "Z0.5"# + str(abs_z)
    #print('Sending: '+ comm)
    s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
    
    #plektrum up
    #comm = "G01 " + "F400"
    #print('Sending: '+ comm)
    #s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print(' : ' + grbl_out.strip())
    
    #comm = "G01 " + "Z-" + str(abs_z)
    #print('Sending: '+ comm)
    #s.write(comm.encode() + '\n'.encode()) # Send g-code block to grbl
    #decode_response()
    #grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    #print(' : ' + grbl_out.strip())
    
    
    time.sleep(1.5);
    #pos()
    #decode_response()
    
  
        

        

    
#------------PROGRAM ------
        
abs_x = str(0)
abs_y = str(0)
abs_z = str(1.5)


# Open grbl serial port of the machine
s = serial.Serial('/dev/tty.usbmodem201912341',115200)
  
# Wake up grbl
s.write("\r\n\r\n".encode())
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input
time.sleep(0.5)

#init plotter movement parameters
calibrate_z_plotter()






time.sleep(1) 
# Close file and serial port
#f.close()

s.close()

print("end program")

