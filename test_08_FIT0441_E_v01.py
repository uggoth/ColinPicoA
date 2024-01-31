program_name = 'test_08_FIT0441_E_v01.py'
description = 'test pulse calibration'

print (program_name, 'starting')

import machine
import utime

def pulse_detected(sender):
    global pulse_count, pulse_endpoint, speed_pin, pulse_pin
    pulse_count += 1
    if pulse_endpoint > 0:
        if pulse_count >= pulse_endpoint:
            pulse_pin.irq(None)
            speed_pin.duty_u16(65535)
            print ('Pulse endpoint ',pulse_endpoint,'reached')

speed_pin_no = 2
pulse_pin_no = 3
direction_pin_no = 4

speed_pin = machine.PWM(machine.Pin(speed_pin_no))
speed_pin.freq(25000)
pulse_pin = machine.Pin(pulse_pin_no, machine.Pin.IN, machine.Pin.PULL_UP)
pulse_pin.irq(pulse_detected, machine.Pin.IRQ_FALLING)
direction_pin = machine.Pin(direction_pin_no, machine.Pin.OUT)
direction_pin.off()

pulse_count = 0
pulses_per_revolution = 270
revolutions = 4
pulse_endpoint = pulses_per_revolution * revolutions

speed_pin.duty_u16(20000)  #  should work at any speed

for i in range(1000):
    utime.sleep_ms(300)
    if pulse_count >= pulse_endpoint:
        break

speed_pin.duty_u16(65535)

pulse_pin.irq(None)

if pulse_count < pulse_endpoint:
    print ('Pulse endpoint not reached. Needs more time')
else:
    print (pulse_count, 'pulses for', revolutions, 'revolutions')
print (program_name, 'finished')

