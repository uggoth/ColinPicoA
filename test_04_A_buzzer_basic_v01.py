module_name = 'test_04_A_buzzer_basic_v01.py'

print (module_name, 'starting')

import machine
import utime

pin = machine.Pin(17)
pwm = machine.PWM(pin)
pwm.freq(244)
pwm.duty_u16(32000)
utime.sleep_ms(500)
pwm.deinit()

print (module_name, 'finished')
