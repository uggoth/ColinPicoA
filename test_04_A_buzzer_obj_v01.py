module_name = 'test_04_A_buzzer_obj_v01.py'

print (module_name, 'starting')

import ThisPico_A_V29 as ThisPico
import utime

my_buzzer = ThisPico.ReversingBuzzer()
if my_buzzer.dip is None:
    print ('DIP not set')
else:
    print (my_buzzer.dip.name,'is',my_buzzer.dip.get())
my_buzzer.play_beep()
utime.sleep_ms(500)
my_buzzer.play_ringtone()
utime.sleep_ms(500)
my_buzzer.close()

print (module_name, 'finished')
