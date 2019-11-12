import logging
import bluepy

class EasySensorTag(bluepy.btle.Peripheral):
    """
    extends the bluepy.btle.Peripheral, so check that for built-in methods
    """
    def __init__(self, addr, debug=logging.INFO):
        bluepy.btle.Peripheral.__init__(self, addr)
        self._mpu9250 = bluepy.sensortag.MovementSensorMPU9250(self)
        self.ir_temp = bluepy.sensortag.IRTemperatureSensorTMP007(self)
        self.accelerometer = bluepy.sensortag.AccelerometerSensorMPU9250(self._mpu9250)
        self.humidity = bluepy.sensortag.HumiditySensorHDC1000(self)
        self.magnetometer = bluepy.sensortag.MagnetometerSensorMPU9250(self._mpu9250)
        self.barometer = bluepy.sensortag.BarometerSensorBMP280(self)
        self.gyroscope = bluepy.sensortag.GyroscopeSensorMPU9250(self._mpu9250)
        self.keypress = bluepy.sensortag.KeypressSensor(self)
        self.lightmeter = bluepy.sensortag.OpticalSensorOPT3001(self)
        self.battery = bluepy.sensortag.BatterySensor(self)
        self.firmware = self.check_firmware()

        self._log = logging.getLogger('EasySensorTag:{}'.format(self.addr))
        self._log.setLevel(debug)
        self._log.debug("Initialized")

    def init_sensors(self):
        self._log.info("Initializing sensors")
        self.ir_temp.enable()
        self.humidity.enable()
        self.barometer.enable()
        self.accelerometer.enable()
        self.magnetometer.enable()
        self.gyroscope.enable()
        self.battery.enable()
        self.keypress.enable()
        self.setDelegate(bluepy.sensortag.KeypressDelegate())
        self.lightmeter.enable()
        self._log.info("Sensors initialized")

    def is_alive(self):
        try:
            self.battery.read()
        except bluepy.btle.BTLEDisconnectError:
            self._log.warn("disconnection error")
            return False
        else:
            return True

    def check_firmware(self):
        try:
            fwVers = self.getCharacteristics(uuid=bluepy.btle.AssignedNumbers.firmwareRevisionString)
            if len(fwVers) >= 1:
                fw = fwVers[0].read().decode("utf-8")
            else:
                fw = u''
        except:
            raise
        return fw

    def read_all(self):
        res = {
            "temperature": self.ir_temp.read(),
            "humidity": self.humidity.read(),
            "barometer": self.barometer.read(),
            "accelerometer": self.accelerometer.read(),
            "magnetometer": self.magnetometer.read(),
            "gyroscope": self.gyroscope.read(),
            "light": self.lightmeter.read(),
            "battery": self.battery.read()
        }

        self._log.debug("read: {}".format(res))
        return res

    def read_temp(self):
        return self.ir_temp.read()

    def read_humid(self):
        return self.humidity.read()

    def read_barom(self):
        return self.barometer.read()

    def read_accel(self):
        return self.accelerometer.read()

    def read_mag(self):
        return self.magnetometer.read()

    def read_gyro(self):
        return self.gyroscope.read()

    def read_light(self):
        return self.lightmeter.read()

    def read_batt(self):
        return self.battery.read()


