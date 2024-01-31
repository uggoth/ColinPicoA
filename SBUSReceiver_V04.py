module_name = 'SBUSReceiver_v04.py'
if __name__ == "__main__":
    print (module_name, 'starting')

import array
import ColObjects_V14 as ColObjects
import machine
import _thread
import utime

class SBUSReceiver:
    def __init__(self, uart):
        self.sbus = uart
        # constants
        self.START_BYTE = b'0f'
        self.END_BYTE = b'00'
        self.SBUS_FRAME_LEN = 25
        self.SBUS_NUM_CHAN = 18
        self.OUT_OF_SYNC_THD = 10
        self.SBUS_NUM_CHANNELS = 18
        self.SBUS_SIGNAL_OK = 0
        self.SBUS_SIGNAL_LOST = 1
        self.SBUS_SIGNAL_FAILSAFE = 2

        # Stack Variables initialization
        self.validSbusFrame = 0
        self.lostSbusFrame = 0
        self.frameIndex = 0
        self.resyncEvent = 0
        self.outOfSyncCounter = 0
        self.sbusBuff = bytearray(1)  # single byte used for sync
        self.sbusFrame = bytearray(25)  # single SBUS Frame
        self.sbusChannels = array.array('H', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])  # RC Channels
        self.isSync = False
        self.startByteFound = False
        self.failSafeStatus = self.SBUS_SIGNAL_FAILSAFE

    def get_rx_channels(self):
        """
        Used to retrieve the last SBUS channels values reading
        :return:  an array of 18 unsigned short elements containing 16 standard channel values + 2 digitals (ch 17 and 18)
        """
        return self.sbusChannels

    def get_rx_channel(self, num_ch):
        """
        Used to retrieve the last SBUS channel value reading for a specific channel
        :param: num_ch: the channel which to retrieve the value for
        :return:  a short value containing
        """
        return self.sbusChannels[num_ch]

    def get_failsafe_status(self):
        """
        Used to retrieve the last FAILSAFE status
        :return:  a short value containing
        """
        return self.failSafeStatus

    def get_rx_report(self):
        """
        Used to retrieve some stats about the frames decoding
        :return:  a dictionary containg three information ('Valid Frames','Lost Frames', 'Resync Events')
        """

        rep = {}
        rep['Valid Frames'] = self.validSbusFrame
        rep['Lost Frames'] = self.lostSbusFrame
        rep['Resync Events'] = self.resyncEvent

        return rep

    def decode_frame(self):

        # TODO: DoubleCheck if it has to be removed
        for i in range(0, self.SBUS_NUM_CHANNELS - 2):
            self.sbusChannels[i] = 0

        # counters initialization
        byte_in_sbus = 1
        bit_in_sbus = 0
        ch = 0
        bit_in_channel = 0

        for i in range(0, 175):  # TODO Generalization
            if self.sbusFrame[byte_in_sbus] & (1 << bit_in_sbus):
                self.sbusChannels[ch] |= (1 << bit_in_channel)

            bit_in_sbus += 1
            bit_in_channel += 1

            if bit_in_sbus == 8:
                bit_in_sbus = 0
                byte_in_sbus += 1

            if bit_in_channel == 11:
                bit_in_channel = 0
                ch += 1

        # Decode Digitals Channels

        # Digital Channel 1
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 0):
            self.sbusChannels[self.SBUS_NUM_CHAN - 2] = 1
        else:
            self.sbusChannels[self.SBUS_NUM_CHAN - 2] = 0

        # Digital Channel 2
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 1):
            self.sbusChannels[self.SBUS_NUM_CHAN - 1] = 1
        else:
            self.sbusChannels[self.SBUS_NUM_CHAN - 1] = 0

        # Failsafe
        self.failSafeStatus = self.SBUS_SIGNAL_OK
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 2):
            self.failSafeStatus = self.SBUS_SIGNAL_LOST
        if self.sbusFrame[self.SBUS_FRAME_LEN - 2] & (1 << 3):
            self.failSafeStatus = self.SBUS_SIGNAL_FAILSAFE

    def get_sync(self):

        if self.sbus.any() > 0:

            if self.startByteFound:
                if self.frameIndex == (self.SBUS_FRAME_LEN - 1):
                    self.sbus.readinto(self.sbusBuff, 1)  # end of frame byte
                    if self.sbusBuff[0] == 0:  # TODO: Change to use constant var value
                        self.startByteFound = False
                        self.isSync = True
                        self.frameIndex = 0
#                        return("found sync")
                else:
                    self.sbus.readinto(self.sbusBuff, 1)  # keep reading 1 byte until the end of frame
                    self.frameIndex += 1
#                    return("start byte found no sync")
            else:
                self.frameIndex = 0
                self.sbus.readinto(self.sbusBuff, 1)  # read 1 byte
                if self.sbusBuff[0] == 15:  # TODO: Change to use constant var value
                    self.startByteFound = True
                    self.frameIndex += 1

    def get_new_data(self):
        """
        This function must be called periodically according to the specific SBUS implementation in order to update
        the channels values.
        For FrSky the period is 300us.
        """

        if self.isSync:
            if self.sbus.any(): # uart.any() returns a 0 or a 1 in this implementation which 'self.sbus.any() >= self.SBUS_FRAME_LEN' would never be true. 3 days working on this. 
                self.sbus.readinto(self.sbusFrame, self.SBUS_FRAME_LEN)  # read the whole frame
                if (self.sbusFrame[0] == 15 and self.sbusFrame[
                    self.SBUS_FRAME_LEN - 1] == 0):  # TODO: Change to use constant var value
                    self.validSbusFrame += 1
                    self.outOfSyncCounter = 0
                    self.decode_frame()
                    return("decode")
                else:
                    self.lostSbusFrame += 1
                    self.outOfSyncCounter += 1

                if self.outOfSyncCounter > self.OUT_OF_SYNC_THD:
                    self.isSync = False
                    self.resyncEvent += 1
                    
            return("is synced")       
        else:
            self.get_sync()

class SBUSReceiverMC6C(ColObjects.ColObj):
    def __init__(self):
        super().__init__('MicroZone mc6c')
        self.tx_pin_no = 0
        self.rx_pin_no = 1
        self.uart_no = 0
        self.baud_rate = 100000
        self.uart = machine.UART(self.uart_no, self.baud_rate, tx = machine.Pin(self.tx_pin_no), rx = machine.Pin(self.rx_pin_no), bits=8, parity=0, stop=2)
        self.sbus = SBUSReceiver(self.uart)
        self.steering_index = 0   #  NOTE: array index starts at zero
        self.throttle_index = 1   #        channel numbers start at one
        self.raise_index = 2
        self.swing_index = 3
        self.switch_index = 4
        self.knob_index = 5
        self.throttle_interpolator = ColObjects.Interpolator('Throttle Interpolator',
                                                [ 100,    201,   900, 1090,  1801,  2000],
                                                [-100.0, -100.0, 0.0,    0.0, 100.0, 100.0])
        self.steering_interpolator = ColObjects.Interpolator('Steering Interpolator',
                                                [100, 693, 1080, 1250, 1500, 2000],
                                                [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
        self.switch_interpolator = ColObjects.Interpolator('Switch 5 Interpolator',
                                                [100, 393, 980, 1220, 1390, 2000],
                                                [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
        self.thread_enable = True
        self.thread_running = False
        self.joystick_raws = [0] * 18
        self.my_thread = _thread.start_new_thread(self.thread_code, ())

    def __str__(self):
        outstring = self.name + '\n'
        outstring += str(self.throttle_interpolator) + '\n'
        outstring += str(self.steering_interpolator) + '\n'
        return outstring

    def thread_code(self):
        self.thread_running = True
        while True:
            if not self.thread_enable:
                break
            utime.sleep_us(300)
            self.sbus.get_new_data()
            self.joystick_raws = self.sbus.get_rx_channels()
        self.thread_running = False

    def get(self):
        max_attempts = 15
        for i in range(max_attempts):
            utime.sleep_us(400)
            steering_raw = self.joystick_raws[self.steering_index]
            if steering_raw > 15:
                break
        if i == max_attempts:
            return None, None
        throttle_raw = self.joystick_raws[self.throttle_index]
        raise_raw = self.joystick_raws[self.raise_index]
        swing_raw = self.joystick_raws[self.swing_index]
        switch_raw = self.joystick_raws[self.switch_index]
        knob_raw = self.joystick_raws[self.knob_index]

        steering_value = self.steering_interpolator.interpolate(steering_raw)
        throttle_value = self.throttle_interpolator.interpolate(throttle_raw)
        raise_value = self.steering_interpolator.interpolate(raise_raw)
        swing_value = self.steering_interpolator.interpolate(swing_raw)
        switch_value = self.switch_interpolator.interpolate(switch_raw)
        knob_value = self.steering_interpolator.interpolate(knob_raw)
        
        return steering_value, throttle_value, raise_value, swing_value, switch_value, knob_value
        
    def close(self):
        self.steering_interpolator.close()
        self.throttle_interpolator.close()
        #self.raise_interpolator.close()
        #self.swing_interpolator.close()
        self.switch_interpolator.close()
        #self.knob_interpolator.close()
        self.thread_enable = False
        utime.sleep_ms(100)
        if self.thread_running:
            print ('error thread not closed')
        super().close()


if __name__ == "__main__":
    import machine
    #my_uart = machine.UART(0, 100000, tx = machine.Pin(0), rx = machine.Pin(1), bits=8, parity=0, stop=2)
    #print (my_uart)
    my_sbus = SBUSReceiverMC6C()
    print (my_sbus)
    my_sbus.close()
    print (module_name, 'finished')
