module_name = 'stop_all_motors_v02.py'
print (module_name)

from machine import Pin, PWM
import utime

lf_speed_pin = PWM(Pin(2))
rf_speed_pin = PWM(Pin(6))
lb_speed_pin = PWM(Pin(10))
rb_speed_pin = PWM(Pin(21))

lf_speed_pin.freq(25000)
rf_speed_pin.freq(25000)
lb_speed_pin.freq(25000)
rb_speed_pin.freq(25000)

stop_duty = 65535

lf_speed_pin.duty_u16(stop_duty)
rf_speed_pin.duty_u16(stop_duty)
lb_speed_pin.duty_u16(stop_duty)
rb_speed_pin.duty_u16(stop_duty)

utime.sleep(0.2)

lf_speed_pin.deinit()
rf_speed_pin.deinit()
lb_speed_pin.deinit()
rb_speed_pin.deinit()

led = Pin(25, Pin.OUT)

for i in range(40):
    led.toggle()
    utime.sleep(0.15)
