module_name = 'test_01_D_switches_v03.py'

import ThisPico_A_V32 as ThisPico
import utime

print (module_name, 'starting')

these_switches = ThisPico.TheseSwitches()

my_switches = these_switches.list

print ("List of switches:")
for switch in my_switches:
    print ('  ',switch.name)
    switch.previous = 'UNKNOWN'

for i in range(100):
    utime.sleep(0.1)
    for switch in my_switches:
        current = switch.get()
        if current != switch.previous:
            print (switch.name, current)
            switch.previous = current

print (module_name, 'finished')
