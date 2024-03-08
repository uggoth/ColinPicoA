module_name = 'test_15_D_command_stream_v03.py'
print (module_name, 'starting')

import ThisPico_A_V36 as ThisPico
CommandStream = ThisPico.CommandStream
import utime

my_handshake = ThisPico.ThisHandshake()
my_stream = CommandStream.CommandStream('HEBE Commands', my_handshake)

print ('*** Close Thonny and start test_15_D_command_stream on Pi ***')
utime.sleep(3)

logging = open('test_15_D.txt','w')

def log(msg):
    global logging
    logging.write(msg + '\n')

log ('Starting\n')

for i in range(10000):
    utime.sleep_ms(1)
    serial_no, command, data = my_stream.get_command()
    if serial_no is not None:
        log(serial_no + command + data)
        if command == 'WHOU':
            my_stream.send(serial_no + 'OKOK' + 'PICOA')
            log('Command WHOU')
        elif command == 'EXIT':
            my_stream.send(serial_no + 'OKOK')
            log('Command EXIT\n')
            break
        else:
            my_stream.send(serial_no + 'BADC')
            log('Command not WHOU')

log('Finished\n')
my_stream.close()
my_handshake.close()
logging.close()