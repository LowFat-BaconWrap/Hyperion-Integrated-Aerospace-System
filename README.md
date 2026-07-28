# Hyperion Integrated Aerospace System

This project is a fun little side project I had during the summer while I was bored. Safe to say it has snowballed far past the point of a "little side project".

SYSTEM ARCHITECTURE:

HYPERION
|
|----- Mission Architecture
|       |- Mission Planning
|       |- Target Selection
|       |- Launch Profile Generation
|       |- Flight Simulation
|       |- Recovery Objectives
|
|
|----- HELIOS
|       |-(Launch Infrastructure)
|       |
|       |- Ground Computation Complex
|       |   |- Raspberry Pi 4
|       |   |- Launch Trajectory Simulation
|       |   |- Wind Data Processing
|       |   |- Guidance Calculations
|       |   |- Mission Control Software
|       |
|       |- Ground Power System
|       |   |- 3S 18650 Battery Pack
|       |   |- IP2368 Charging System
|       |   |- Buck Conversion System
|       |   |- Power Distribution
|       |
|       |- Launch Control System
|       |   |- Arduino Nano Controller
|       |   |- Pan/Tilt Control Firmware
|       |   |- Safety Interlocks
|       |   |- Launch State Monitoring
|       |
|       |- Launch Platform
|       |   |- Dual NEMA 17 Pan/Tilt Assembly
|       |   |- Mechanical Alignment System
|       |   |- Launch Rail Assembly
|       |
|       |- Ground Support Systems
|           |
|           |- Wind Measurement System
|           |   |- Anemometer
|           |   |- Wind Direction Measurement
|           |   |- MCP3008 ADC
|           |   |- Weather Data Processing
|           |
|           |- Ground Telemetry Station
|           |   |- RF Receiver
|           |   |- Mission Data Display
|           |   |- Flight Monitoring
|           |
|           |- Simulation Environment
|               |- Flight Dynamics Model
|               |- Atmospheric Model
|               |- Weather Model
|               |- Launch Optimization
|
|
|----- PHAETHON
|       |-(Flight Vehicle)
|       |
|       |- AETHON
|       |   |-(Flight Computer / Avionics Core)
|       |   |
|       |   |- Arduino Nano Flight Computer
|       |   |- Embedded Flight Software
|       |   |- MPU-6050 Inertial Measurement Unit
|       |   |- BME280 Atmospheric Sensor
|       |   |- Sensor Interface
|       |   |- Sensor Fusion Algorithms
|       |   |- Flight State Estimation
|       |   |- Mission Logic
|       |   |- Flight Data Logging
|       |   |- Recovery Deployment Logic
|       |
|       |
|       |- EOUS
|       |   |-(Communication & Telemetry System)
|       |   |
|       |   |- RF Transceiver
|       |   |- Antenna System
|       |   |- Telemetry Downlink
|       |   |- Data Packet Processing
|       |   |- Ground Station Communication
|       |   |- Link Quality Monitoring
|       |   |- Error Handling
|       |
|       |
|       |- PYROIS
|       |   |-(Propulsion System)
|       |   |
|       |   |- Motor Assembly
|       |   |- Motor Cartridge Interface
|       |   |- Motor Retention System
|       |   |- Hotswap Motor System
|       |   |- Ignition Interface
|       |   |- Thermal Protection
|       |   |- Propulsion Mounting Structure
|       |   |- Thrust Characterization
|       |   |- Motor Performance Data
|       |
|       |
|       |- PHLEGON
|       |   |-(Onboard Power System)
|       |   |
|       |   |- LiPo Battery System
|       |   |- Battery Protection System
|       |   |- Voltage Regulation
|       |   |- Power Distribution
|       |   |- Current Monitoring
|       |   |- Battery Telemetry
|       |   |- Thermal Monitoring
|       |   |- Avionics Power Rail
|       |   |- RF Power Rail
|       |   |- Power Management System
|       |   |- Low Voltage Protection
|       |
|       |
|       |- Recovery System
|           |-(Flight Recovery System)
|           |
|           |- Parachute Assembly
|           |- Deployment Mechanism
|           |- Recovery Hardware
|           |- Landing Protection
|           |- Recovery Tracking
