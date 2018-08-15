# -*- coding:utf-8 -*-
import serial
import subprocess
import atexit
import datetime
from time import sleep
try:
    import getrpimodel
except ImportError as e:
    import sys
    sys.path.append('/home/pi/.local/lib/python3.5/site-packages')
    import getrpimodel

# setting
detect_intarval_sec = 60

if getrpimodel.model() == "3 Model B":
    serial_dev = '/dev/ttyS0'
    stop_getty = 'sudo systemctl stop serial-getty@ttyS0.service'
    start_getty = 'sudo systemctl start serial-getty@ttyS0.service'
else:
    serial_dev = '/dev/ttyAMA0'
    stop_getty = 'sudo systemctl stop serial-getty@ttyAMA0.service'
    start_getty = 'sudo systemctl start serial-getty@ttyAMA0.service'


def _mh_z19():
    ser = serial.Serial(serial_dev,
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1.0)
    while True:
        result = ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
        s = ser.read(9)
        if len(s) >= 4 and s[0] == 255 and s[1] == 134:
            timestamp = datetime.datetime.now().timestamp()
            co2 = (int(s[2])*256) + int(s[3])
            print({'timestamp': dt, 'co2': co2})
        sleep(detect_intarval_sec)


def _stop():
    p = subprocess.call(stop_getty, stdout=subprocess.PIPE, shell=True)


def _start():
    p = subprocess.call(start_getty, stdout=subprocess.PIPE, shell=True)


def main():
    _stop()
    _mh_z19()


if __name__ == '__main__':
    atexit.register(_start)
    main()
