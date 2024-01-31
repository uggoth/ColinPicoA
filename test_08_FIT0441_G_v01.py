module_name = 'test_08_FIT0441_G_v01.py'
description = 'test ThisPico object'

print (module_name, 'starting')

import ThisPico_A_V28 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_train = ThisPico.ThisDriveTrain()

loops = 3
for i in range(loops):
    print ('loop',i+1,'of',loops)
    my_train.drive(50,0)
    utime.sleep(1)
    my_train.stop()
    utime.sleep(1)
    my_train.drive(60,60)
    utime.sleep(1)
    my_train.stop()
    utime.sleep(1)

my_train.close()

print (module_name, 'finished')

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
