# Power Architecture
This explains the layout of the whole system's power architecture

```mermaid
graph LR

H[IP2368<br>USB-to-Battery]

H --> HELIOS[BMS<br>Battery Protection]

HELIOS --> BUCK[Buck Cpnverter<br>Lowers voltage]
HELIOS --> NEMA1[NEMA17 Driver/Motor<br>Turns the launch platform]
HELIOS --> NEMA2[NEMA 17 Driver/Motor<br>Changes launch angle]

BUCK --> RPI[RPi4B<br>Main Computer]

RPI --> ARDUINO[Arduino Nano<br>Main launch controller]
```

Here's a more technical and detailed description of the power layout. Keep in mind this schematic is SUPER simplified and only show the rough idea of the power system.
[Helios Power Schematic.pdf](https://github.com/user-attachments/files/30455144/Helios.Power.Schematic.pdf)
