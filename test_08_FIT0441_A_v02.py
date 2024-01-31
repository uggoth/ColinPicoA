program_name = 'test_08_FIT0441_A_v02.py'
description = 'test basic movement'

print (program_name, 'starting')

import machine
import utime

which_motor = 'Left Front'
#which_motor = 'Right Front'
#which_motor = 'Left Rear'
#which_motor = 'Right Rear'

motors = {'Left Front':[2,3,4],'Right Front':[6,7,8],'Left Rear':[10,11,12],'Right Rear':[21,20,19]}
speed_pin_no = motors[which_motor][0]
pulse_pin_no = motors[which_motor][1]
direction_pin_no = motors[which_motor][2]

speed_pin = machine.PWM(machine.Pin(speed_pin_no))
speed_pin.freq(25000)
pulse_pin = machine.Pin(pulse_pin_no, machine.Pin.IN, machine.Pin.PULL_UP)
direction_pin = machine.Pin(direction_pin_no, machine.Pin.OUT)
direction_pin.off()

speed_pin.duty_u16(16000)
utime.sleep(1)
speed_pin.duty_u16(65535)
utime.sleep(1)
direction_pin.on()
speed_pin.duty_u16(16000)
utime.sleep(1)
speed_pin.duty_u16(65535)

print (program_name, 'finished')

