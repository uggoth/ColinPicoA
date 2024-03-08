module_name = 'main_zyderbot_rc_v04.py'
module_description = 'Joystick Mixing'
module_last_worked_on_date = '20240307'
print (module_name, 'starting')

import ThisPico_A_V34 as ThisPico
SBUSReceiver = ThisPico.SBUSReceiver
ColObjects = ThisPico.ColObjects
import Motor_V04 as Motor
import utime
import machine

my_headlight = ThisPico.ThisHeadlight()
my_mc6c = SBUSReceiver.SBUSReceiverMC6C()

lf_speed_pin_no     = 2   # blue
lf_direction_pin_no = 4   # yellow
motor_lf = Motor.FIT0441BasicMotor('Left Front', lf_direction_pin_no, lf_speed_pin_no)

lb_speed_pin_no     = 10
lb_direction_pin_no = 12
motor_lb = Motor.FIT0441BasicMotor('Left Back', lb_direction_pin_no, lb_speed_pin_no)

rf_speed_pin_no     = 6   # blue
rf_direction_pin_no = 8   # yellow
motor_rf = Motor.FIT0441BasicMotor('Right Front', rf_direction_pin_no, rf_speed_pin_no)

rb_speed_pin_no     = 21
rb_direction_pin_no = 19
motor_rb = Motor.FIT0441BasicMotor('Right Back', rb_direction_pin_no, rb_speed_pin_no)

motor_list = [motor_lf, motor_lb, motor_rf, motor_rb]

for motor in motor_list:
    motor.stop()

interval = 10
first_time = True
i=0

while True:
    i += 1
    utime.sleep_us(300)
    lf_level, rf_level, lb_level, rb_level = my_mc6c.get_tank_mix()
    motor_lf.run(-lf_level)
    motor_rf.run(rf_level)
    motor_lb.run(-lb_level)
    motor_rb.run(rb_level)
    if sum([lf_level, lb_level]) > sum([rf_level, rb_level]):
        my_headlight.spr()
    elif sum([lf_level, lb_level]) < sum([rf_level, rb_level]):
        my_headlight.spl()
    elif sum([lf_level, rf_level, lb_level, rb_level]) >= 0:
        my_headlight.fwd()
    else:
        my_headlight.rev()
    steering_value, throttle_value, updown_value, swing_value, switch_value, knob_value = my_mc6c.get()
    if ((switch_value is not None) and (switch_value < 0)):
        break

motor_lf.close()
motor_rf.close()
motor_lb.close()
motor_rb.close()
my_headlight.close()
my_mc6c.close()

utime.sleep(1)

print (module_name, 'finished')