module_name = 'test_08_FIT0441_F_v01.py'
description = 'test object'

print (module_name, 'starting')

import Motor_V03 as Motor
ColObjects = Motor.ColObjects
import utime

name = 'Right Front'
speed_pin_no = 6
pulse_pin_no = 7
direction_pin_no = 8
#name = 'Right Back'
#speed_pin_no = 21
#pulse_pin_no = 20
#direction_pin_no = 19
#name = 'Left Back'
#speed_pin_no = 10
#pulse_pin_no = 11
#direction_pin_no = 12
#name = 'Left Front'
#speed_pin_no = 2
#pulse_pin_no = 3
#direction_pin_no = 4
test_motor = Motor.FIT0441Motor(name, direction_pin_no, speed_pin_no, pulse_pin_no)

speed = 50
start = test_motor.get_pulses()

test_motor.clk(50)
utime.sleep(1)
test_motor.stop()
utime.sleep(1)
test_motor.anti(50)
utime.sleep(1)
test_motor.stop()

finish = test_motor.get_pulses()
diff = finish - start

test_motor.close()

print (test_motor.name,diff,'pulses')

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
