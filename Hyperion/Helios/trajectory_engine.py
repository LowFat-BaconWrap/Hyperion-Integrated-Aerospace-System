import numpy as np
import json
import os

class LookupTableMaker():
    def __init__(self, ground_wind_speed):
        self.MAX_LEGAL_CEILING = 15000
        self.wind_speed_ground = float(ground_wind_speed)
        self.tripod_height = 1.5
        self.de_marris_rc = 0.14

        self.step_size = 0.1

        self.slot_amount = int(np.ceil(self.MAX_LEGAL_CEILING/self.step_size)) + 1
        self.wind_table_array = np.zeros(self.slot_amount)

        self._generate_sky_table()

    def _generate_sky_table(self):

        for index in range(self.slot_amount):
            altitude_raw = index * self.step_size

            if altitude_raw < self.tripod_height:
                altitude = self.tripod_height
            else:
                altitude = altitude_raw

            calculated_windspeed = self.wind_speed_ground * ((altitude/self.tripod_height) ** self.de_marris_rc)
            self.wind_table_array[index] = calculated_windspeed

    def fetch_windspeed(self, current_height):

        if current_height <= 0:
            return self.wind_table_array[0]
        if current_height >= self.MAX_LEGAL_CEILING:
            return self.wind_table_array[-1]

        lookup_index = int(current_height/self.step_size)
        return self.wind_table_array[lookup_index]

class FlightCalculator:

    def __init__(self, motor_name, total_mass, drag_coefficient, radius, rail_length):
        self.motor_name = motor_name.upper()
        self.cd = drag_coefficient
        self.total_mass = total_mass
        self.frontal_area = np.pi * radius ** 2
        self.rail_length = float(rail_length)

        self.departure_velocity = 0.0
        self.is_stably_launched = False

        database_path = "motors/registry.json"

        try:
            with open(database_path, "r") as file:
                registry = json.load(file)

            if self.motor_name in registry:
                motor_data = registry[self.motor_name]
            else:
                print("motor not found")

            self.time_points = np.array(motor_data["time_points"])
            self.thrust_points = np.array(motor_data["thrust_points"])
            self.propellant_kg = float(motor_data["propellant_kg"])
            self.burn_time = float(motor_data["burn_time"])

        except Exception as error:
            print("motor data retrieval failed")

        self.dry_mass = self.total_mass - self.propellant_kg


    def _get_thrust(self, elapsed_time):

        if elapsed_time >= self.burn_time:
            return 0.0
        else:
            return np.interp(elapsed_time, self.time_points, self.thrust_points)

    def _calculate_derivatives(self, altitude, velocity, elapsed_time, ground_air_density, windspeed_table):

        if altitude < 0.0:
            altitude = 0.0
        if velocity < 0.0 and elapsed_time <= self.burn_time:
            velocity = 0.0

        air_density = ground_air_density * np.exp(-altitude / 8500)

        angle_of_attack = 0
        current_fuel = 0
        dynamic_cd = self.cd

        thrust = self._get_thrust(elapsed_time)
        if elapsed_time < self.burn_time:
            burnt_fuel_ratio = elapsed_time / self.burn_time
            current_fuel = self.propellant_kg * (1.0 - burnt_fuel_ratio)
            mass = self.dry_mass + current_fuel

            cg_stability_multiplier = 1.0 + ( 0.35 * burnt_fuel_ratio)
        else:
            mass = self.dry_mass

            cg_stability_multiplier = 1.35

        if altitude < self.rail_length:

            tilt_ratio = 0.0
            dynamic_cd = self.cd

        else:

            live_crosswind = windspeed_table.fetch_windspeed(altitude)
            effective_wind_force = live_crosswind * cg_stability_multiplier
            tilt_ratio = min(effective_wind_force / 45.0, 0.35)

            if velocity > 2.0:
                angle_of_attack = np.arctan(live_crosswind / velocity)
            else:
                angle_of_attack = 0.0

            induced_drag_factor = 2.5
            dynamic_cd = self.cd + (induced_drag_factor * (angle_of_attack ** 2))

            if self.departure_velocity == 0.0 and velocity > 0.0:
                self.departure_velocity = velocity
                if self.departure_velocity > 13.4:
                    self.is_stably_launched = True

        effective_vert_thrust = thrust * (1.0 - tilt_ratio)

        drag_magnitude = 0.5 * air_density * (velocity ** 2) * dynamic_cd * self.frontal_area
        drag_vector = np.sign(velocity) * drag_magnitude

        EARTH_RADIUS = 6378137
        gravity = 9.80665 * ((EARTH_RADIUS / (EARTH_RADIUS + altitude)) ** 2)

        net_up_force = effective_vert_thrust
        net_down_force = drag_vector + (mass * gravity)

        if altitude <= 0.001 and net_up_force <= net_down_force:
            acceleration = 0
            velocity = 0
        else:
            acceleration = (net_up_force - net_down_force) / mass

        self.tracked_Cd_history = dynamic_cd
        self.tracked_tilt_history = angle_of_attack
        self.tracked_mass_history = mass
        self.tracked_propellant_history = current_fuel

        return velocity, acceleration

    def calculate_rk4_ascent(self, ground_air_density, windspeed_table):

        self.time_history = []
        self.altitude_history = []
        self.velocity_history = []
        self.acceleration_history = []

        self.windspeed_history = []
        self.Cd_history = []
        self.tilt_history = []
        self.mass_history = []
        self.propellant_history = []

        self.departure_velocity = 0.0
        self.is_stably_launched = False

        dt = 0.01
        altitude = 0.0
        velocity = 0.0
        elapsed_time = 0.0

        while True:

            self.time_history.append(elapsed_time)
            self.altitude_history.append(altitude)
            self.velocity_history.append(velocity)

            self.windspeed_history.append(windspeed_table.fetch_windspeed(altitude))

            v1, a1 = self._calculate_derivatives(altitude, velocity, elapsed_time, ground_air_density, windspeed_table)
            v2, a2 = self._calculate_derivatives(altitude + v1*dt/2, velocity + a1*dt/2, elapsed_time + dt/2, ground_air_density, windspeed_table)
            v3, a3 = self._calculate_derivatives(altitude + v2*dt/2, velocity + a2*dt/2, elapsed_time + dt/2, ground_air_density, windspeed_table)
            v4, a4 = self._calculate_derivatives(altitude + v3*dt, velocity + a3*dt, elapsed_time + dt, ground_air_density, windspeed_table)

            self.Cd_history.append(self.tracked_Cd_history)
            self.tilt_history.append(self.tracked_tilt_history)
            self.mass_history.append(self.tracked_mass_history)
            self.propellant_history.append(self.tracked_propellant_history)

            altitude += (dt / 6.0) * (v1 + 2*v2 + 2*v3 + v4)
            velocity += (dt / 6.0) * (a1 + 2*a2 + 2*a3 + a4)
            self.acceleration_history.append(a1)
            elapsed_time += dt

            if velocity <= 0.0 and elapsed_time > self.burn_time:
                break

        return min(altitude, 1500.0)
        
    def calculate_descent_drift(self, simulated_apogee, parachute_rate_ms, windspeed_table):
        dt = 0.01
        current_altitude = float(simulated_apogee)
        current_time = self.time_history[-1]
        total_drift_meters = 0.0

        EARTH_RADIUS = 6378137
        gravity = 9.80665 * ((EARTH_RADIUS / (EARTH_RADIUS + current_altitude)) ** 2)

        descent_velocity = 0
        terminal_velocity = -float(parachute_rate_ms)

        while current_altitude > 0:
            windvelocity = windspeed_table.fetch_windspeed(current_altitude)

            total_drift_meters += windvelocity * dt

            if descent_velocity > terminal_velocity:
                descent_velocity -= gravity * dt
                acceleration = -gravity

                if descent_velocity < terminal_velocity:
                    descent_velocity = terminal_velocity
                    acceleration = 0
            else:
                descent_velocity = terminal_velocity
                acceleration = 0

            current_altitude += descent_velocity * dt
            current_time += dt

            self.time_history.append(current_time)
            self.altitude_history.append(current_altitude)
            self.velocity_history.append(descent_velocity)
            self.acceleration_history.append(acceleration)
            self.windspeed_history.append(windvelocity)
            self.Cd_history.append(self.cd)
            self.tilt_history.append(0)
            self.mass_history.append(self.dry_mass)
            self.propellant_history.append(0)

        return total_drift_meters

    def solve_for_launch_angle(self, target_distance, ground_air_density, windspeed_table):

        low_angle = 0
        high_angle = 20
        best_angle = 0
        tolerance = .05

        for iteration in range(15):

            test_angle = (low_angle + high_angle) / 2

            apogee = self.calculate_rk4_ascent(ground_air_density=ground_air_density, windspeed_table=windspeed_table)
            drift = self.calculate_descent_drift(simulated_apogee=apogee,   parachute_rate_ms=6, windspeed_table=windspeed_table)

            predicted_landing_distance = (np.tan(np.radians(test_angle)) * apogee) - drift

            error = predicted_landing_distance - target_distance

            if abs(error) < tolerance:
                best_angle = test_angle
                break

            if error < 0:
                low_angle = test_angle
            else:
                high_angle = test_angle

            best_angle = test_angle

        return best_angle



if __name__ == "__main__":

    windtable = LookupTableMaker(ground_wind_speed=4)
    calc = FlightCalculator(motor_name="F15", total_mass=.4, drag_coefficient=.5, radius=.021, rail_length=2.4)

    apogee = calc.calculate_rk4_ascent(ground_air_density=1.185, windspeed_table=windtable)
    drift = calc.calculate_descent_drift(simulated_apogee=apogee, parachute_rate_ms=6, windspeed_table=windtable)
    angle = calc.solve_for_launch_angle(target_distance=-400, ground_air_density=1.185, windspeed_table=windtable)

    print(apogee)
    print(drift)
    print(angle)


