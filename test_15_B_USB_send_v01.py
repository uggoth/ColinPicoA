module_name = 'test_15_B_USB_send_v01.py'
print (module_name, 'starting')

import CommandStreamPico_v02 as CommandStream
import utime

my_stream = CommandStream.CommandStream()

if not my_stream.valid:
    print ('**** Failed to open stream')

print ('*** close Thonny now ***')
print ('*** and start the reader test_15_B_USB_reader ***')
utime.sleep(5)

for i in range(50):
    utime.sleep(0.5)
    my_stream.send('loop ' + str(i))

my_stream.close()
print (module_name, 'finished')