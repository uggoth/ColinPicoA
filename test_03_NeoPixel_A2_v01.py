module_name = 'test_03_NeoPixel_A2_v01.py'
print (module_name, 'starting')

import NeoPixel_v12 as NeoPixel
import utime

my_headlight = NeoPixel.NeoPixel(name='headlights', pin_no=15, no_pixels=7, mode='GRBW')
my_headlight.sectors['rear_centre'] = [0,0]
my_headlight.sectors['rear_rim'] = [1,6]

my_headlight.fill_sector('rear_centre','blue')
my_headlight.show()
utime.sleep_ms(1000)

my_headlight.fill_sector('rear_rim','red')
my_headlight.show()
utime.sleep_ms(1000)

my_headlight.pixels[2:5] = my_headlight.colours['green']
my_headlight.show()
utime.sleep_ms(1000)

my_headlight.close()
print (module_name, 'finishing')
