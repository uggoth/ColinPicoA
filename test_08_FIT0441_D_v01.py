program_name = 'test_08_FIT0441_D_v01.py'
description = 'test pulse calibration'

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

pulse_count = 0

def pulse_detected(sender):
    global pulse_count
    pulse_count += 1

pulse_pin.irq(pulse_detected, machine.Pin.IRQ_FALLING)

revolutions = 4.6  #  determined by observation

start = pulse_count
speed_pin.duty_u16(40000)
utime.sleep(5)
speed_pin.duty_u16(65535)

end = pulse_count
diff = end - start
pulses_per_rev = int (diff / revolutions)
print ('pulses_per_rev', pulses_per_rev, ' (nominal is 270)')
pulse_pin.irq(None)

print (program_name, 'finished')

