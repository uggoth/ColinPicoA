module_name = 'test_03_NeoPixel_A1_v01.py'
print (module_name, 'starting')

import NeoPixel_v12 as NeoPixel
import utime

my_headlight = NeoPixel.NeoPixel(name='headlights', pin_no=18, no_pixels=14, mode='GRB')
my_headlight.sectors['front_right_centre'] = [0,0]
my_headlight.sectors['front_right_rim'] = [1,6]
my_headlight.sectors['front_left_centre'] = [7,7]
my_headlight.sectors['front_left_rim'] = [8,13]

my_headlight.fill_sector('front_left_centre','blue')
my_headlight.show()
utime.sleep_ms(1000)

my_headlight.fill_sector('front_right_rim','red')
my_headlight.show()
utime.sleep_ms(1000)

my_headlight.pixels[8:14] = my_headlight.colours['green']
my_headlight.show()
utime.sleep_ms(1000)

my_headlight.close()
print (module_name, 'finishing')
