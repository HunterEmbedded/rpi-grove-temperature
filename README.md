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

Use RPi Imager to load a full 64bit image and then boot.

Once booted log in and clone this repository.

```
git clone https://github.com/HunterEmbedded/rpi-grove-temperature.git
```


Follow instructions at https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi/#installation to
install the repository and enable the I2C.

Follow the instructions for the **Virtual Environment** to set up the venv, activate it and install the RPi python packages.

Then follow the **For beginner or library user** pane to install the grove repository in a virtual environment.
For clarity this is the following instruction

```
curl -sL https://github.com/Seeed-Studio/grove.py/raw/master/install.sh | bash -s -- --user-local --bypass-gui-installation
```

Now that the grove repository is installed we can update the default script for the sensor to the modified version that supports
two sensors and writes the data to file

```
cp rpi-grove-temperature/grove_temperature_humidity_sensor_sht3x.py env/lib/python3.11/site-packages/grove/grove_temperature_humidity_sensor_sht3x.py

```

Run the script with command *grove_temperature_humidity_sht31*. The output to screen and to file ~/temperature-log.txt will show time and the two temperature samples

```
(env) XXXX@raspberrypi:~ $ grove_temperature_humidity_sht31
10:40:40,25.4,27.6,

10:40:50,25.4,27.7,

10:41:00,25.4,27.7,
```
