module_prefix = 'test_15_F_command_motors'
module_name = module_prefix + '_v01.py'
print (module_name, 'starting')

import ThisPico_A_V31 as ThisPico
import CommandStreamPico_v02 as CommandStream
import utime

my_train = ThisPico.ThisDriveTrain()
my_stream = CommandStream.CommandStream()

print ('*** Close Thonny and start ' + module_prefix + ' on Pi ***')
utime.sleep(9)

logging = open(module_prefix + '.txt','w')

def log(msg):
    global logging
    logging.write(msg + '\n')

log (module_prefix + ' starting')

for i in range(10000):
    utime.sleep_ms(1)
    message = my_stream.get()
    if message:
        log(message)
        command = message[0:4]
        if len(message) > 7:
            parameter = int(message[4:8])
        else:
            parameter = None
        if 'WHOU' == command:
            log('OK')
            my_stream.send('PICOA')
        elif 'MFWD' == command:
            log('OK')
            if parameter is not None:
                log(str(parameter))
                my_stream.send('Motors Forward Speed ' + str(parameter))
                my_train.fwd(parameter)
            else:
                my_stream.send('Motors Forward Default Speed')
                my_train.fwd()
        elif 'MREV' == command:
            log('OK')
            if parameter is not None:
                log(str(parameter))
                my_stream.send('Motors Reverse Speed ' + str(parameter))
                my_train.rev(speed)
            else:
                my_stream.send('Motors Reverse Default Speed')
                my_train.rev()
        elif 'MSTP' == command:
            log('OK')
            my_stream.send('Motors Stopping')
            my_train.stop()
        elif 'EXIT' == command:
            log('OK')
            my_stream.send('Exiting')
            break
        else:
            ermsg = '*** Not Known ***'
            log(ermsg)
            my_stream.send(ermsg)

log (module_prefix + ' finished')
logging.close()