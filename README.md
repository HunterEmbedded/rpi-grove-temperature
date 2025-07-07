# rpi-grove-temperature
Basic python script to read two SHT31 temp sensors and store to file.

## Hardware
It uses the [Grove Base Hat](https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi/#features) and
two [Grove temperature sensors](https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-SHT31.html).
Only two of these sensors can be used as they only support I2C addresses 0x44 or 0x45.

The second sensor must have a hardware modification to change the address to 0x45.
Resistor R2 must be removed and then TP2 must be connected to TP6 to pull ADDR pin of SHT31 high to select
the alternative I2C address of 0x45.

## Software


