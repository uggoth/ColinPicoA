module_prefix = 'test_15_F_command_motors'
module_name = module_prefix + '_v01.py'
print (module_name, 'starting')

import ThisPico_A_V34 as ThisPico
import CommandStreamPico_v02 as CommandStream
import utime
SBUSReceiver = ThisPico.SBUSReceiver
ColObjects = ThisPico.ColObjects
import Motor_V04 as Motor
import machine

my_stream = CommandStream.CommandStream()
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

logging = open(module_prefix + '.txt','w')

def log(msg):
    global logging
    logging.write(msg + '\n')

log (module_prefix + ' starting')

interval = 10
first_time = True
i=0

print ('Close Thonny and run   test_15_G_command_stream   on the Pi')

while True:
    i += 1
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
    if i%interval == 0:
        message = my_stream.get()
        if message:
            log(message)
            serial_no_string = message[0:4]
            command = message[4:8]
            if len(message) > 7:
                parameter = int(message[8:12])
            else:
                parameter = None
            if 'WHOU' == command:
                log('OK')
                my_stream.send('PICOA')
            elif 'EXIT' == command:
                log('OK')
                my_stream.send('Exiting')
                break
            else:
                ermsg = '*** Not Known ***'
                log(ermsg)
                my_stream.send(ermsg)

my_stream.close()
my_headlight.close()
my_mc6c.close()

log (module_prefix + ' finished')
logging.close()