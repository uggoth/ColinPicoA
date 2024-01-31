module_name = 'test_08_DriveTrain_B_v01.py'

import ThisPico_A_V31 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

utime.sleep(1)
my_train = ThisPico.ThisDriveTrainWithHeadlights()
my_train.fwd()
utime.sleep(1)
my_train.stop()
utime.sleep(1)
my_train.rev()
utime.sleep(1)
my_train.stop()
utime.sleep(1)
my_train.spl()
utime.sleep(1)
my_train.stop()
utime.sleep(1)
my_train.spr()
utime.sleep(1)
my_train.stop()
utime.sleep(1)

my_train.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
