import serial
import time


class dp800():

    def __init__(self, port):
        self.port = port
        self.connecting = False
        self.ser = []

    def connect(self):
        if not self.connecting:
            self.ser = serial.Serial(self.port, baudrate=9600, timeout=3)
            if self.ser.is_open:
                self.connecting = True

    def disconnect(self):
        if self.connecting:
            self.ser.close()
            self.connecting = False

    def write(self, message):
        if not self.connecting:
            self.connect()
        if self.connecting:
            self.ser.write(str.encode(message) + b'\r\n')
            time.sleep(0.032)

    def output(self, ch, onoff):

        if not ((ch == 1) or (ch == 2) or (ch == 3)):
            raise ValueError('Please select CH 1~3')

        if onoff:
            self.write(':OUTP CH' + str(ch) + ',ON')
        else:
            self.write(':OUTP CH' + str(ch) + ',OFF')

    def ch(self, mych):

        if not ((mych == 1) or (mych == 2) or (mych == 3)):
            raise ValueError('Please select CH 1~3')

        command = ':INST CH' + str(mych)
        self.write(command)

    def v(self, mych, voltage):

        self.ch(mych)
        command = ':VOLT ' + (str(float(voltage)) + '0000')[:4]
        self.write(command)

    def v_protect(self, mych, voltage):

        self.ch(mych)
        command = ':VOLT:PROT ' + (str(float(voltage)) + '0000')[:4]
        self.write(command)
        command = ':VOLT:PROT:STAT ON'
        self.write(command)

    def v_protect_off(self, mych):

        self.ch(mych)
        command = ':VOLT:PROT:STAT OFF'
        self.write(command)

    def i(self, mych, current):

        self.ch(mych)
        command = ':CURR ' + (str(float(current)) + '0000')[:4]
        self.write(command)

    def i_protect(self, mych, current):

        self.ch(mych)
        command = ':CURR:PROT ' + (str(float(current)) + '0000')[:4]
        self.write(command)
        command = ':CURR:PROT:STAT ON'
        self.write(command)

    def i_protect_off(self, mych):

        self.ch(mych)
        command = ':CURR:PROT:STAT OFF'
        self.write(command)
