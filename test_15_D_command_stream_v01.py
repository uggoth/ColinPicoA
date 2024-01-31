module_name = 'test_15_D_command_stream_v01.py'
print (module_name, 'starting')

import CommandStreamPico_v02 as CommandStream
import utime

my_stream = CommandStream.CommandStream()

print ('*** Close Thonny and start test_15_D_command_stream on Pi ***')
utime.sleep(9)

logging = open('test_15_D.txt','w')

def log(msg):
    global logging
    logging.write(msg + '\n')

for i in range(10000):
    utime.sleep_ms(1)
    message = my_stream.get()
    if message:
        log(message)
        if 'WHOU' == message[0:4]:
            log('OK')
            my_stream.send('PICOA')
        elif 'EXIT' == message[0:4]:
            log('OK')
            my_stream.send('Exiting')
            break
        else:
            ermsg = '*** Not Known ***'
            log(ermsg)
            my_stream.send(ermsg)
            
logging.close()