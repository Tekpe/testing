#!/usr/bin/env python
# -*- coding: utf_8 -*-

import sys
from pynput.keyboard import Key, Controller
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial
import time
import linuxcnc

CNCcommand = linuxcnc.command()
CNCstat = linuxcnc.stat()


'''PORT = 0'''
PORT = '/dev/ttyS0'
keyboard = Controller()


def main():
    """main"""
    # Create the server
    server = modbus_rtu.RtuServer(serial.Serial(PORT))

    try:
        server.start()
        slave_1 = server.add_slave(1)
        slave_1.add_block('0x', cst.COILS, 0, 100)
        slave_1.add_block('4x', cst.HOLDING_REGISTERS, 0, 500)
        slave_1.set_values(block_name='4x', address=99, values=1)
        plus = True
        minus = True
        FlagXl = False
        FlagXr = False
        FlagYl = False
        FlagYr = False
        FlagZl = False
        FlagZr = False
        while True:
			//X CW
			if slave_1.get_values(block_name='0x', address=10)[0]:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False, 1 , 1000)
				Flag1=True
			elif not slave_1.get_values(block_name='0x', address=10)[0] and Flag1:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False, 1 , 0)
				Flag1=False
			
			//X CCW
			if slave_1.get_values(block_name='0x', address=11)[0]:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False , 1 , -1000)	
				Flag2=True	
			elif not slave_1.get_values(block_name='0x', address=11)[0] and Flag2:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False, 1 , 0)		
				Flag2=False

			
			//Y CW
			if slave_1.get_values(block_name='0x', address=12)[0]:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False, 1 , 1000)
				Flag1=True
			elif not slave_1.get_values(block_name='0x', address=12)[0] and Flag1:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False, 1 , 0)
				Flag1=False
			
			//Y CCW
			if slave_1.get_values(block_name='0x', address=13)[0]:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False , 1 , -1000)	
				Flag2=True	
			elif not slave_1.get_values(block_name='0x', address=13)[0] and Flag2:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False, 1 , 0)		
				Flag2=False
				
				
			//Z CW
			if slave_1.get_values(block_name='0x', address=14)[0]:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False, 1 , 1000)
				Flag1=True
			elif not slave_1.get_values(block_name='0x', address=14)[0] and Flag1:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False, 1 , 0)
				Flag1=False
			
			//Z CCW
			if slave_1.get_values(block_name='0x', address=15)[0]:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False , 1 , -1000)	
				Flag2=True	
			elif not slave_1.get_values(block_name='0x', address=15)[0] and Flag2:
				CNCcommand.mode(linuxcnc.MODE_MANUAL)
				CNCcommand.wait_complete()
				CNCcommand.jog(linuxcnc.JOG_CONTINUOUS, False, 1 , 0)		
				Flag2=False
			
			
			
			
			
			if slave_1.get_values(block_name='0x', address=0)[0] and plus:
				CNCcommand.mode(linuxcnc.MODE_MDI)
				CNCcommand.wait_complete()
				newValue=slave_1.get_values(block_name='4x', address=0)[0]+1000
				if newValue>24000:
					newValue=24000
				slave_1.set_values(block_name='4x', address=0, values=newValue)
				plus=False
				message='n30 s{value} m3'.format(value=newValue)
				CNCcommand.mdi(message)

			elif not slave_1.get_values(block_name='0x', address=0)[0] and not plus:
				plus=True

			if slave_1.get_values(block_name='0x', address=1)[0] and minus:
				CNCcommand.mode(linuxcnc.MODE_MDI)
				CNCcommand.wait_complete()
				newValue=slave_1.get_values(block_name='4x', address=0)[0]-1000
				if newValue<0:
					newValue=0
				slave_1.set_values(block_name='4x', address=0, values=newValue)
				minus=False
				message='n30 s{value} m3'.format(value=newValue)
				CNCcommand.mdi(message)

			elif not slave_1.get_values(block_name='0x', address=1)[0] and not minus:
				minus = True
			time.sleep(0.01)
    finally:
        server.stop()


if __name__ == "__main__":
    main()
