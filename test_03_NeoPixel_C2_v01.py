module_name = 'test_03_NeoPixel_C_v01.py'
print (module_name, 'starting')

import ThisPico_A_V32 as ThisPico
import utime

my_rear_light = ThisPico.ThisRearLight()

my_rear_light.OK()
utime.sleep_ms(1000)

my_rear_light.bad()
utime.sleep_ms(1000)

my_rear_light.close()
print (module_name, 'finishing')
