import dearpygui.dearpygui as dpg
import numpy as np
import time

from trajectory_engine import LookupTableMaker, FlightCalculator

dpg.create_context()
dpg.create_viewport(title='HYPERION TELEMETRY DECK', width=1265, height=800, resizable=False)
dpg.setup_dearpygui()

time_history_data = [0.0]
altitude_history_data = [0.0]
velocity_history_data = [0.0]
acceleration_history_data = [0.0]
Cd_history_data = [0.0]
windspeed_history_data = [0.0]
tilt_history_data = [0.0]
mass_history_data = [0.0]
propellant_history_data = [0.0]

def trigger_calculations():

    wind_speed = dpg.get_value(input_windspeed)
    motor_name = dpg.get_value(input_motor)
    total_mass = dpg.get_value(input_mass)
    drag_coefficient = dpg.get_value(input_cd)
    radius = dpg.get_value(input_radius)
    rail_length = dpg.get_value(input_rail)

    windspeed_table = LookupTableMaker(ground_wind_speed=wind_speed)
    calculation = FlightCalculator(
        motor_name=motor_name,
        total_mass=total_mass,
        drag_coefficient=drag_coefficient,
        radius=radius,
        rail_length=rail_length
        )

    apogee = calculation.calculate_rk4_ascent(ground_air_density=1.185, windspeed_table=windspeed_table)
    drift = calculation.calculate_descent_drift(simulated_apogee=apogee, parachute_rate_ms=6, windspeed_table=windspeed_table)

    x_coord = calculation.time_history
    y_coord = calculation.altitude_history
    y1_coord = calculation.velocity_history
    y2_coord = calculation.acceleration_history
    aero_y_coord = calculation.windspeed_history
    aero_y1_coord = calculation.Cd_history
    aero_y2_coord = calculation.tilt_history
    mass_y_coord = calculation.mass_history
    mass_y1_coord = calculation.propellant_history

    dpg.set_value("Altitude Profile Line", [x_coord, y_coord])
    dpg.set_value("Velocity Profile Line", [x_coord, y1_coord])
    dpg.set_value("Acceleration Profile Line", [x_coord, y2_coord])
    dpg.fit_axis_data("X AXIS")
    dpg.fit_axis_data("Y AXIS")
    dpg.set_axis_limits_constraints("X AXIS", 0.0, max(x_coord))
    dpg.set_axis_limits_constraints("Y AXIS", min(y2_coord) - 10, max(y_coord) + 25)

    dpg.set_value("Windspeed Profile Line", [x_coord, aero_y_coord])
    dpg.set_value("Drag Coefficient Profile Line", [x_coord, aero_y1_coord])
    dpg.set_value("Tilt Profile Line", [x_coord, aero_y2_coord])
    dpg.fit_axis_data("AERO X AXIS")
    dpg.fit_axis_data("AERO Y AXIS")
    dpg.fit_axis_data("DRAG X AXIS")
    dpg.fit_axis_data("DRAG Y AXIS")
    dpg.set_axis_limits_constraints("AERO X AXIS", 0.0, max(x_coord))
    dpg.set_axis_limits_constraints("AERO Y AXIS", min(aero_y2_coord) - 1, max(aero_y_coord) + 5)
    dpg.set_axis_limits_constraints("DRAG X AXIS", 0.0, max(x_coord))
    dpg.set_axis_limits_constraints("DRAG Y AXIS", min(aero_y1_coord) - 1, max(aero_y1_coord) + 1)

    dpg.set_value("Mass Profile Line", [x_coord, mass_y_coord])
    dpg.set_value("Propellant Profile Line", [x_coord, mass_y1_coord])
    dpg.fit_axis_data("MASS X AXIS")
    dpg.fit_axis_data("MASS Y AXIS")
    dpg.set_axis_limits_constraints("MASS X AXIS", 0.0, max(x_coord))
    dpg.set_axis_limits_constraints("MASS Y AXIS", min(mass_y1_coord) - 1, max(mass_y_coord) + 1)

    dpg.set_value("Apogee", f"Calculated apogee: {apogee:.2f} meters")
    dpg.set_value("Drift", f"Calculated Drift: {drift:.2f} meters downwind")
    dpg.set_value("Departure Velocity", f"Rail clear velocity: {calculation.departure_velocity:.2f} m/s (~{calculation.departure_velocity * 2.23694:.1f} mph) ")

    if calculation.is_stably_launched:
        dpg.set_value("stability", "launch stable, rail clear velocity good")
    else:
        dpg.set_value("stability", "launch unstable, rail clear velocity bad")

with dpg.window(label="PARAMETER INPUT", width=380, height=760, no_close=True, no_move=True):
    dpg.add_text("Parameter input")

    input_motor = dpg.add_input_text(label="Motor Name")
    input_mass = dpg.add_input_float(label="Wet Mass (kg)", format="%.3f")
    input_cd = dpg.add_input_float(label="Base Drag (Cd)", format="%.2f")
    input_radius = dpg.add_input_float(label="Radius (m)", format="%.4f")
    input_rail = dpg.add_input_float(label="Rail Length (m)", format="%.1f")
    input_windspeed = dpg.add_input_float(label="TEMPORARY WINDSPEED. REMOVE ONCE ANEMOMETER WORKS. KEEP AT 4", format="%.1f")

    dpg.add_spacer(height=15)
    dpg.add_button(label="Run Solver", callback=trigger_calculations, width=340, height=40)

    dpg.add_spacer(height=20)
    dpg.add_text("Readouts")
    dpg.add_text("N/A", tag="Apogee")
    dpg.add_text("N/A", tag="Drift")
    dpg.add_text("N/A", tag="Departure Velocity")
    dpg.add_text("N/A", tag="stability")

with dpg.window(label="GRAPH", width=870, height=760, no_close=True, pos=[380, 0], no_move=True):

    with dpg.tab_bar(tag="flight_variables"):
        with dpg.tab(label="KINEMATICS"):
            dpg.add_spacer(height=5)
            with dpg.plot(label="Plot", width=850, height=700):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="X AXIS")
                with dpg.plot_axis(dpg.mvYAxis, label="Altitude (m)", tag="Y AXIS"):
                    dpg.add_line_series(time_history_data, altitude_history_data, label="Altitude (m)", tag="Altitude Profile Line")
                    dpg.add_line_series(time_history_data, velocity_history_data, label="Velocity (m/s)", tag="Velocity Profile Line")
                    dpg.add_line_series(time_history_data, acceleration_history_data, label="Acceleration (m/s²)", tag="Acceleration Profile Line")
        with dpg.tab(label="AERODYNAMICS"):
            dpg.add_spacer(height=5)
            with dpg.plot(label="Plot", width=500, height=300):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="AERO X AXIS")
                with dpg.plot_axis(dpg.mvYAxis, label="Windspeed (m/s) & Tilt Angle", tag="AERO Y AXIS"):
                    dpg.add_line_series(time_history_data, windspeed_history_data, label="Windspeed (m/s)", tag="Windspeed Profile Line")
                    dpg.add_line_series(time_history_data, tilt_history_data, label="Tilt (degrees)", tag="Tilt Profile Line")
            dpg.add_spacer(height=2)
            with dpg.plot(label="Drag Coefficient", width=500, height=300):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="DRAG X AXIS")
                with dpg.plot_axis(dpg.mvYAxis, label="Drag Coefficient", tag="DRAG Y AXIS"):
                    dpg.add_line_series(time_history_data, Cd_history_data, label="Drag Coefficient (Cd)", tag="Drag Coefficient Profile Line")
        with dpg.tab(label="MASS"):
            dpg.add_spacer(height=5)
            with dpg.plot(label="Plot", width=850, height=700):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="MASS X AXIS")
                with dpg.plot_axis(dpg.mvYAxis, label="Mass (kg)", tag="MASS Y AXIS"):
                    dpg.add_line_series(time_history_data, mass_history_data, label="Mass (kg)", tag="Mass Profile Line")
                    dpg.add_line_series(time_history_data, propellant_history_data, label="Propellant Mass (kg)", tag="Propellant Profile Line")

dpg.show_viewport()

FPS = 60
FRAME_DURATION = 1 / FPS

while dpg.is_dearpygui_running():

    frame_start = time.time()

    dpg.render_dearpygui_frame()

    frame_execution_time = time.time() - frame_start
    if frame_execution_time < FRAME_DURATION:
        time.sleep(FRAME_DURATION - frame_execution_time)

dpg.destroy_context()