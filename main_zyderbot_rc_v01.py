module_name = 'main_zyderbot_rc_v01.py'
module_description = 'Joystick Mixing'
print (module_name, 'starting')

import SBUSReceiver_V05 as SBUSReceiver
ColObjects = SBUSReceiver.ColObjects
import Motor_V04 as Motor
import utime
import machine

def array_abs(input):
    output_array = []
    for element in input:
        output_array.append(abs(element))
    return output_array

def mix(inputs):
    #print (' ')
    size = len(inputs)
    if ((size > 3) or (size < 2)):
        raise ColObjects.ColError('Mixer must have inputs: steering, throttle, slew[optional]')
    inputs_abs = array_abs(inputs)
    biggest_in = max(inputs_abs)
    total_in = sum(inputs_abs)
    if total_in == 0:
        return 0,0,0,0
    #print ('total_in', total_in)
    # motors are in the order: Left Front, Right Front, Left Back, Right Back
    steering = inputs[0]
    throttle = inputs[1]
    fwd_levels = [throttle, throttle, throttle, throttle]
    #print ('fwd_levels', fwd_levels)
    spin_levels = [steering, -steering, steering, -steering]
    #print ('spin_levels', spin_levels)
    fwd_abs = array_abs(fwd_levels)
    #print ('fwd_abs', fwd_abs)
    spin_abs = array_abs(spin_levels)
    total_out = sum(fwd_abs) + sum(spin_abs)
    slew_levels = [0,0,0,0]
    if size == 3:
        slew = inputs[2]
        slew_levels = [slew, slew, -slew, -slew]
        slew_abs = array_abs(slew_levels)
        total_out = total_out + sum(slew_abs)
    #print ('total_out', total_out)
    ratio_a = 1.0
    #print ('ratio', ratio)
    lf_level = (fwd_levels[0] + spin_levels[0] + slew_levels[0]) * ratio_a
    rf_level = (fwd_levels[1] + spin_levels[1] - slew_levels[1]) * ratio_a
    lb_level = (fwd_levels[2] + spin_levels[2] + slew_levels[2]) * ratio_a
    rb_level = (fwd_levels[3] + spin_levels[3] - slew_levels[3]) * ratio_a
    output_abs = array_abs([lf_level, rf_level, lb_level, rb_level])
    biggest_out = max(output_abs)
    ratio_b = biggest_in / biggest_out
    lf_level = lf_level * ratio_b
    rf_level = rf_level * ratio_b
    lb_level = lb_level * ratio_b
    rb_level = rb_level * ratio_b
    return lf_level, rf_level, lb_level, rb_level

uart_no = 0
tx_pin_no = 0
rx_pin_no = 1
baud_rate = 100000
my_uart = machine.UART(uart_no, baud_rate, tx = machine.Pin(tx_pin_no), rx = machine.Pin(rx_pin_no), bits=8, parity=0, stop=2)
my_mc6c = SBUSReceiver.SBUSReceiver(my_uart)

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

#  values obtained from test_18_SBUS_A
min_steering = 692
min_throttle = 601
min_slew = 569

mid_steering = 1094
mid_throttle = 1000
mid_slew = 976

max_steering = 1486
max_throttle = 1401
max_slew = 1369

dead_zone = 10

steering_interpolator = ColObjects.Interpolator('Steering Interpolator',
                                    [100, min_steering, mid_steering - dead_zone, mid_steering + dead_zone, max_steering, 2000],
                                    [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
throttle_interpolator = ColObjects.Interpolator('Throttle Interpolator',
                                    [100, min_throttle, mid_throttle - dead_zone, mid_throttle + dead_zone, max_throttle, 2000],
                                    [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
slew_interpolator = ColObjects.Interpolator('Slew Interpolator',
                                    [100, min_slew, mid_slew - dead_zone, mid_slew + dead_zone, max_slew, 2000],
                                    [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])

interval = 100
first_time = True

for i in range(50000):
    utime.sleep_us(300)
    my_mc6c.get_new_data()
    channels = my_mc6c.get_rx_channels()
    if channels[0] < 15:  #  ignore bad values
        continue
    if ((i % interval) == 0):
        steering_raw = channels[0]
        throttle_raw = channels[1]
        slew_raw = channels[3]
        steering_in = steering_interpolator.interpolate(steering_raw)
        throttle_in = throttle_interpolator.interpolate(throttle_raw)
        slew_in = slew_interpolator.interpolate(slew_raw)
        lf_level, rf_level, lb_level, rb_level = mix([steering_in, throttle_in, slew_in])
        #print (lf_level, rf_level, lb_level, rb_level)
        motor_lf.run(-lf_level)
        motor_rf.run(rf_level)
        motor_lb.run(-lb_level)
        motor_rb.run(rb_level)

motor_lf.stop()
motor_rf.stop()
motor_lb.stop()
motor_rb.stop()

print (module_name, 'finished')