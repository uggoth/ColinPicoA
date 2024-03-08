module_name = 'main_zyderbot_rc_v04.py'
module_description = 'Joystick Mixing'
print (module_name, 'starting')

import ThisPico_A_V33 as ThisPico
import SBUSReceiver_V05 as SBUSReceiver
ColObjects = SBUSReceiver.ColObjects
import Motor_V04 as Motor
import utime
import machine

def array_abs(input):
    output_array = []
    for element in input:
        if element is None:
            output_array.append(0)
        else:
            output_array.append(abs(element))
    return output_array

def mix(inputs):
    #print (' ')
    size = len(inputs)
    if ((size > 3) or (size < 2)):
        raise ColObjects.ColError('Mixer must have inputs: steering, throttle, crab[optional]')
    for i in range(len(inputs)):
        if inputs[i] is None:
            inputs[i] = 0
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
    crab_levels = [0,0,0,0]
    if size == 3:
        crab = inputs[2]
        crab_levels = [crab, crab, -crab, -crab]
        crab_abs = array_abs(crab_levels)
        total_out = total_out + sum(crab_abs)
    #print ('total_out', total_out)
    ratio_a = 1.0
    #print ('ratio', ratio)
    lf_level = (fwd_levels[0] + spin_levels[0] + crab_levels[0]) * ratio_a
    rf_level = (fwd_levels[1] + spin_levels[1] - crab_levels[1]) * ratio_a
    lb_level = (fwd_levels[2] + spin_levels[2] + crab_levels[2]) * ratio_a
    rb_level = (fwd_levels[3] + spin_levels[3] - crab_levels[3]) * ratio_a
    output_abs = array_abs([lf_level, rf_level, lb_level, rb_level])
    biggest_out = max(output_abs)
    ratio_b = biggest_in / biggest_out
    lf_level = lf_level * ratio_b
    rf_level = rf_level * ratio_b
    lb_level = lb_level * ratio_b
    rb_level = rb_level * ratio_b
    return lf_level, rf_level, lb_level, rb_level

my_headlight = ThisPico.ThisHeadlight()
my_blue_button = ThisPico.BlueButton()
my_buzzer = ThisPico.ReversingBuzzer()

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

for motor in motor_list:
    motor.stop()

#  values obtained from test_18_SBUS_A
min_steering = 692
min_throttle = 601
min_crab = 569
min_switch = 201

mid_steering = 1094
mid_throttle = 1000
mid_crab = 976
mid_switch = 1004

max_steering = 1486
max_throttle = 1401
max_crab = 1369
max_switch = 1801


dead_zone = 15

steering_interpolator = ColObjects.Interpolator('Steering Interpolator',
                                    [100, min_steering, mid_steering - dead_zone, mid_steering + dead_zone, max_steering, 2000],
                                    [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
throttle_interpolator = ColObjects.Interpolator('Throttle Interpolator',
                                    [100, min_throttle, mid_throttle - dead_zone, mid_throttle + dead_zone, max_throttle, 2000],
                                    [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
crab_interpolator = ColObjects.Interpolator('crab Interpolator',
                                    [100, min_crab, mid_crab - dead_zone, mid_crab + dead_zone, max_crab, 2000],
                                    [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
switch_interpolator = ColObjects.Interpolator('Switch Interpolator',
                                    [100, min_switch, mid_switch - dead_zone, mid_switch + dead_zone, max_switch, 2000],
                                    [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])

interval = 10
first_time = True
i=0

while True:
    i += 1
    utime.sleep_us(300)
    my_mc6c.get_new_data()
    channels = my_mc6c.get_rx_channels()
    if channels[0] < 15:  #  ignore bad values
        continue
    if ((i % interval) == 0):
        switch_raw = channels[4]
        switch_in = switch_interpolator.interpolate(switch_raw)
        if switch_in < 0:
            print ('STOPPING', switch_in)
            break
        steering_raw = channels[0]
        steering_in = steering_interpolator.interpolate(steering_raw)
        throttle_raw = channels[1]
        throttle_in = throttle_interpolator.interpolate(throttle_raw)
        crab_raw = channels[3]
        crab_in = crab_interpolator.interpolate(crab_raw)
        if switch_in > 0:
            temp = crab_in
            crab_in = -steering_in
            steering_in = -temp
        lf_level, rf_level, lb_level, rb_level = mix([steering_in, throttle_in, crab_in])
        #print (lf_level, rf_level, lb_level, rb_level)
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
        

motor_lf.stop()
motor_rf.stop()
motor_lb.stop()
motor_rb.stop()
my_headlight.close()

print (module_name, 'finished')