module_name = 'test_08_Side_B_v01.py'

import ThisPico_A_V28 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

test_side = ThisPico.ThisRightSide()
print ('--- AFTER INSTANTIATION --')
print (ColObjects.ColObj.str_allocated())

def runit(speed):
    print (speed)
    test_side.drive(speed)
    utime.sleep(3)
    test_side.stop()
    utime.sleep(1)

runit(50)
runit(-50)
runit(5)
runit(0)

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
