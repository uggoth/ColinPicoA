module_name = 'test_15_A_handshake_v01.py'
print (module_name, 'starting')

import utime
import machine

toggle = 0
handshake = machine.Pin(15,machine.Pin.OUT)
handshake.value(toggle)

led_onboard=machine.Pin(25, machine.Pin.OUT)

for i in range(19):
    utime.sleep_ms(500)
    toggle = 1 - toggle
    handshake.value(toggle)
    led_onboard.value(toggle)


