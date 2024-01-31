module_name = 'test_18_SBUS_H_drive_v01.py'
description = 'testing object with headlights'
import ThisPico_A_V32 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_sbus = ThisPico.ThisSbusReceiver()
print (my_sbus)
my_train = ThisPico.ThisDriveTrainWithHeadlights()
print (my_train)

bad_gets = 0

while True:
    utime.sleep_ms(10)
    return_values = my_sbus.get()
    if None in return_values:
        bad_gets += 1
        continue
    else:
        steering_value, throttle_value, raise_value, swing_value, switch_value, knob_value = return_values
    if switch_value < 0:
        break
    elif switch_value > 0:
        my_train.headlights_enabled = True
    else:
        my_train.headlights_enabled = False
    if throttle_value is None:
        continue
    else:
        my_train.drive(throttle_value, steering_value)

my_train.headlight.off()
my_train.stop()
my_train.close()
my_sbus.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
