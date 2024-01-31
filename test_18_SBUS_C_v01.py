module_name = 'test_18_SBUS_C_v01.py'
module_description = 'Joystick Mixing'
print (module_name, 'starting')

test_inputs = [[100,0,0],[0,100,0],[100,100,0],[0,0,100],[100,0],[50,50],[50,0]]

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
    #print ('total_in', total_in)
    # motors are in the order: Left Front, Right Front, Left Back, Right Back
    throttle = inputs[0]
    steering = inputs[1]
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
    rf_level = (fwd_levels[1] + spin_levels[1] + slew_levels[1]) * ratio_a
    lb_level = (fwd_levels[2] + spin_levels[2] + slew_levels[2]) * ratio_a
    rb_level = (fwd_levels[3] + spin_levels[3] + slew_levels[3]) * ratio_a
    output_abs = array_abs([lf_level, rf_level, lb_level, rb_level])
    biggest_out = max(output_abs)
    ratio_b = biggest_in / biggest_out
    lf_level = lf_level * ratio_b
    rf_level = rf_level * ratio_b
    lb_level = lb_level * ratio_b
    rb_level = rb_level * ratio_b
    return lf_level, rf_level, lb_level, rb_level

for test_case in test_inputs:
    print ('IN:',test_case, ',  OUT:', mix(test_case))

print (module_name, 'finished')

