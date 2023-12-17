#!/usr/bin/env python
"""\
Simple g-code streaming script for grbl
"""
 
import serial
import time
 
# Open grbl serial port
s = serial.Serial('/dev/tty.usbmodem201912341',115200)
 
# Open g-code file
f = open('tekne1.gcode','r');
 
# Wake up grbl
s.write("\r\n\r\n".encode())
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input
 
# Stream g-code to grbl
for line in f:
    l = line.strip() # Strip all EOL characters for streaming
    print('Sending: ' + l)
    s.write(l.encode() + '\n'.encode()) # Send g-code block to grbl
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())
 
# Wait here until grbl is finished to close serial port and file.
#raw_input("  Press <Enter> to exit and disable grbl.")

time.sleep(2) 
# Close file and serial port
f.close()

s.close()
