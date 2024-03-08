module_name = 'test_15_C_USB_reader_v02.py'
print (module_name, 'starting')

import ThisPico_A_V36 as ThisPico
CommandStream = ThisPico.CommandStream
import utime

my_handshake = ThisPico.ThisHandshake()
my_stream = CommandStream.CommandStream('HEBE Commands', my_handshake)

if not my_stream.valid:
    print ('**** Failed to open stream')

print ('*** Close Thonny and start sender test_15_C_USB_sender on Pi ***')
utime.sleep(3)

logging = open('test_15_C.txt','w')
logging.write('Starting\n')
for i in range(9):
    utime.sleep_ms(1000)
    message = my_stream.get(400).upper()
    if not message:
        continue
    logging.write(message)
logging.write('Finished\n')
my_stream.close()
my_handshake.close()
logging.close()
