import ThisPico_A_V30 as ThisPico
import utime

module_name = 'test_01_B_IR_Sensors_v01.py'

print (module_name, "starting")

lrir = ThisPico.LRIR()
rrir = ThisPico.RRIR()

my_irs = [lrir, rrir]

for sensor in my_irs:
    sensor.previous = 'UNKNOWN'

for i in range(1900):
    utime.sleep(0.01)
    for sensor in my_irs:
        current = sensor.get()
        name = sensor.name
        if current != sensor.previous:
            sensor.previous = current
            print (name,'is now',current)

print (module_name, "finished")
