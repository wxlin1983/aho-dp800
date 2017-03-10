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
            time.sleep(0.064)

    def read(self, second=0):

        if not self.connecting:
            raise Exception('Communication failed.')
        if self.connecting:
            time.sleep(second)
            return self.ser.read(self.ser.in_waiting)

    def getch(self, ch):

        if not ((ch == 1) or (ch == 2) or (ch == 3)):
            raise ValueError('Please select CH 1~3')

        return 'CH' + str(ch)

    def ch(self, mych):

        command = ':INST ' + self.getch(mych)
        self.write(command)

    def output(self, ch, onoff):

        if onoff:
            self.write(':OUTP ' + self.getch(ch) + ',ON')
        else:
            self.write(':OUTP ' + self.getch(ch) + ',OFF')

    def v(self, mych, voltage):

        self.ch(mych)
        command = ':VOLT ' + (str(float(voltage)) + '0000')[:4]
        self.write(command)

    def protect_v(self, mych, voltage):

        self.ch(mych)
        command = ':VOLT:PROT ' + (str(float(voltage)) + '0000')[:4]
        self.write(command)
        command = ':VOLT:PROT:STAT ON'
        self.write(command)

    def protect_v_off(self, mych):

        self.ch(mych)
        command = ':VOLT:PROT:STAT OFF'
        self.write(command)

    def i(self, mych, current):

        self.ch(mych)
        command = ':CURR ' + (str(float(current)) + '0000')[:4]
        self.write(command)

    def protect_i(self, mych, current):

        self.ch(mych)
        command = ':CURR:PROT ' + (str(float(current)) + '0000')[:4]
        self.write(command)
        command = ':CURR:PROT:STAT ON'
        self.write(command)

    def protect_i_off(self, mych):

        self.ch(mych)
        command = ':CURR:PROT:STAT OFF'
        self.write(command)

    def read_i(self, mych):

        command = ':MEAS:CURR? ' + self.getch(mych)
        self.write(command)
        return self.read(0)
