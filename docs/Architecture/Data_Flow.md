# Data Transfer Throughout Hyperion

This file explains the flow of data throughout the system as a whole. This helps with anybody who want to make edits to the current system,, attach new sensors, or figure out if removing something cripples the entire system.

Data flow through Helios:

Wind Sensors > ADC > RPi4 > Flight Simulation (Generates launch angle and azimuth) > Arduino > NEMA 17 Motors (Sets launchpad to the recieved angle and azimuth from RPi)

Date flow though Phaethon:

MPU6050 + BME280 > Aethon > Eous RF Link > Helios
