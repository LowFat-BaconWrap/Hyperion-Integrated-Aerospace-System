import time
import math
import numpy as np
import spidev
import digitalio
import board
import adafruit_bme280

class HeliosHardwareDrivers:
    def __init__(self, mcp_cs_pin=board.D7):

        self.spi = spidev.SpiDev()
        self.spi.open(0, 1)
        self.spi.max_speed_hz = 1350000

        