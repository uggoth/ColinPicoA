module_name = 'test_15_C_USB_reader_v01.py'
print (module_name, 'starting')

import CommandStreamPico_v02 as CommandStream
import utime

my_stream = CommandStream.CommandStream()

print ('*** Close Thonny and start sender test_15_C_USB_sender on Pi ***')
utime.sleep(9)

logging = open('test_15_C.txt','w')

for i in range(19):
    utime.sleep_ms(1000)
    message = my_stream.get(400).upper()
    if not message:
        continue
    logging.write(message)

my_stream.close()

