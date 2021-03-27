
import sys
from pynput.keyboard import Key, Controller
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial
import time


'''PORT = 0'''
PORT = 'COM3'
keyboard = Controller()


def main():
    """main"""
    # Create the server
    server = modbus_rtu.RtuServer(serial.Serial(PORT))

    try:
        server.start()
        slave_1 = server.add_slave(1)
        slave_1.add_block('0x', cst.COILS, 0, 100)
        slave_1.add_block('4x', cst.HOLDING_REGISTERS, 0, 100)
        plus = True
        minus = True
        while True:
            if slave_1.get_values(block_name='0x', address=0)[0] and plus:
                slave_1.set_values(block_name='4x', address=0, values=slave_1.get_values(block_name='4x', address=0)[0]+1)
                keyboard.press('+')
                keyboard.release('+')
                plus=False

            elif not slave_1.get_values(block_name='0x', address=0)[0] and not plus:
                plus=True

            if slave_1.get_values(block_name='0x', address=1)[0] and minus:
                slave_1.set_values(block_name='4x', address=0, values=slave_1.get_values(block_name='4x', address=0)[0]-1)
                keyboard.press('-')
                keyboard.release('-')
                minus=False

            elif not slave_1.get_values(block_name='0x', address=1)[0] and not minus:
                minus = True

            time.sleep(0.01)
    finally:
        server.stop()


if __name__ == "__main__":
    main()
