{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw16840\paperh23820\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python\
"""\\\
Simple g-code streaming script for grbl\
"""\
 \
import serial\
import time\
 \
# Open grbl serial port\
s = serial.Serial('/dev/tty.usbmodem201912341',115200)\
 \
# Open g-code file\
f = open('tekne1.gcode','r');\
 \
# Wake up grbl\
s.write("\\r\\n\\r\\n".encode())\
time.sleep(2)   # Wait for grbl to initialize\
s.flushInput()  # Flush startup text in serial input\
 \
# Stream g-code to grbl\
for line in f:\
    l = line.strip() # Strip all EOL characters for streaming\
    print('Sending: ' + l)\
    s.write(l.encode() + '\\n'.encode()) # Send g-code block to grbl\
    grbl_out = s.readline().decode()  # Wait for grbl response with carriage return\
    print(' : ' + grbl_out.strip())\
 \
# Wait here until grbl is finished to close serial port and file.\
#raw_input("  Press <Enter> to exit and disable grbl.")\
\
time.sleep(2) \
# Close file and serial port\
f.close()\
\
s.close()\
}