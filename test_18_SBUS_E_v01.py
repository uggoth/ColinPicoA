module_name = 'test_18_SBUS_E_v01.py'
description = 'testing object'
import ThisPico_A_V32 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_sbus = ThisPico.ThisSbusReceiver()
print (my_sbus)

for i in range(19):
    return_values = my_sbus.get()
    if return_values[0] is None:
        continue
    else:
        print (return_values)
    utime.sleep(0.5)

my_sbus.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
