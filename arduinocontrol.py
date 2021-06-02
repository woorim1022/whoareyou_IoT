from pyfirmata import Arduino, util
import time


board=Arduino('/dev/ttyACM0')
pin10 = board.get_pin('d:10:p')
pin11 = board.get_pin('d:11:p')

while True:
    board.digital[13].write(1)
    board.digital[12].write(1)
    pin10.write(0.6)
    pin11.write(0.6)
    time.sleep(1)
    board.digital[13].write(0)
    board.digital[12].write(0)
    pin10.write(0.6)
    pin11.write(0.6)
    time.sleep(1)