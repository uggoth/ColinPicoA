module_name = 'test_03_NeoPixel_C_v01.py'
print (module_name, 'starting')

import ThisPico_A_V31 as ThisPico
import utime

my_headlight = ThisPico.ThisHeadlight()

my_headlight.fwd()
utime.sleep_ms(1000)

my_headlight.rev()
utime.sleep_ms(1000)

my_headlight.spl()
utime.sleep_ms(1000)

my_headlight.spr()
utime.sleep_ms(1000)

my_headlight.close()
print (module_name, 'finishing')
