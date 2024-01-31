program_name = 'test_08_FIT0441_B_v01.py'
description = 'test speed min max'

print (program_name, 'starting')

import machine
import utime

speed_pin_no = 2
pulse_pin_no = 3
direction_pin_no = 4

speed_pin = machine.PWM(machine.Pin(speed_pin_no))
speed_pin.freq(25000)
pulse_pin = machine.Pin(pulse_pin_no, machine.Pin.IN, machine.Pin.PULL_UP)
direction_pin = machine.Pin(direction_pin_no, machine.Pin.OUT)
direction_pin.off()

speed_pin.duty_u16(6000)
utime.sleep(1)
speed_pin.duty_u16(65535)
utime.sleep(1)
speed_pin.duty_u16(56000)
utime.sleep(1)
speed_pin.duty_u16(65535)

print (program_name, 'finished')

