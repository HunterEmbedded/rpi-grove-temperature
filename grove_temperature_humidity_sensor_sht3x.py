#!/usr/bin/env python
#
# Library for Grove - Temperature & Humidity Sensor (SHT31)
# (https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-SHT3-p-2655.html)
#

'''
## License

The MIT License (MIT)

Copyright (C) 2018  Seeed Technology Co.,Ltd. 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
import time
import datetime
import os

from grove.i2c import Bus


def CRC(data):
    crc = 0xff
    for s in data:
        crc ^= s
        for _ in range(8):
            if crc & 0x80:
                crc <<= 1
                crc ^= 0x131
            else:
                crc <<= 1
    return crc


class GroveTemperatureHumiditySensorSHT3x(object):

    # need to explicitly initialise bus to 1 
    def __init__(self, address=0x44, bus=1):
        self.address = address
        # I2C bus
        self.bus = Bus(bus)

    def read(self):
        # high repeatability, clock stretching disabled
        self.bus.write_i2c_block_data(self.address, 0x24, [0x00])

        # measurement duration < 16 ms
        time.sleep(0.016)

        # read 6 bytes back
        # Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
        data = self.bus.read_i2c_block_data(self.address, 0x00, 6)

        if data[2] != CRC(data[:2]):
            raise ValueError("temperature CRC mismatch")
        if data[5] != CRC(data[3:5]):
            raise ValueError("humidity CRC mismatch")


        temperature = data[0] * 256 + data[1]
        celsius = -45 + (175 * temperature / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        return celsius, humidity


def main():

    # initialise the two sensors at addr 0x44 and 0x45
    sensor1 = GroveTemperatureHumiditySensorSHT3x(0x44, 1)
    sensor2 = GroveTemperatureHumiditySensorSHT3x(0x45, 1)

    logFileName = os.environ['HOME'] + "/temperature-log.txt"

    with open(logFileName,'w') as f:
        while True:
            temperature1, humidity1 = sensor1.read()
            temperature2, humidity2 = sensor2.read()

            T1_str = "{:.1f}".format(temperature1)
            T2_str = "{:.1f}".format(temperature2)
 
            TimeNow = time.strftime("%H:%M:%S")
            outputString = ",".join([TimeNow, T1_str, T2_str, '\n'])

            print(outputString)
            f.write(outputString)
            f.flush()
            time.sleep(10)


if __name__ == "__main__":
    main()

