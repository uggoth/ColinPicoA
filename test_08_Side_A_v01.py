module_name = 'test_08_Side_A_v01.py'

import ThisPico_A_V28 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

test_side = ThisPico.ThisRightSide()
print ('--- AFTER INSTANTIATION --')
print (ColObjects.ColObj.str_allocated())

test_side.fwd(50)
utime.sleep(1)
test_side.stop()
utime.sleep(1)
test_side.rev(50)
utime.sleep(1)
test_side.stop()
utime.sleep(1)
test_side.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
