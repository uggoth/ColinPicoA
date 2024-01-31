module_name = 'test_18_SBUS_G_drive_v01.py'
description = 'testing object'
import ThisPico_A_V32 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_sbus = ThisPico.ThisSbusReceiver()
print (my_sbus)
my_train = ThisPico.ThisDriveTrain()
print (my_train)

bad_gets = 0
for i in range(100):
    return_values = my_sbus.get()
    if None in return_values:
        bad_gets += 1
        continue
    else:
        steering_value, throttle_value, raise_value, swing_value, switch_value, knob_value = return_values
        my_train.drive(throttle_value, steering_value)
    utime.sleep_ms(100)
print (bad_gets,'bad gets')

my_train.stop()
my_train.close()
my_sbus.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
