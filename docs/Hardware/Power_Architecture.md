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
## More Technical Schematic
Keep in mind this schematic is SUPER simplified and only show the rough idea of the power system.

<img width="3508" height="2481" alt="Helios Power Schematic" src="https://github.com/user-attachments/assets/2cbaa79c-c77c-4016-ac6e-15b591680cdb" />
