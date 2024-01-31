module_name = 'test_00_Volts_A_v01.py'

my_volts = machine.ADC(29)
conversion_factor = 0.000164
raw = my_volts.read_u16()
volts = raw * conversion_factor

print (module_name, volts)
