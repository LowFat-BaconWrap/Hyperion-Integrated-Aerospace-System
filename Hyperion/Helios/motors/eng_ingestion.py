import os
import json

class AutomatedIngestionPipeline:
    def __init__(self):

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.eng_folder = os.path.join(self.script_dir, "eng_files")
        self.output_json = os.path.join(self.script_dir, "registry.json")

        self.registry = {}

    def compile_motors(self):

        if not os.path.exists(self.eng_folder):
            print("no eng folder twin :[")
            return

        all_files = os.listdir(self.eng_folder)
        targets = [f for f in all_files if f.lower().endswith('.eng')]
        print("found target files")

        for filename in targets:
            file_path = os.path.join(self.eng_folder, filename)
            self._parse_eng_file(file_path)

        with open(self.output_json, "w") as json_file:
            json.dump(self.registry, json_file, indent=2)
            print("json dumped")

    def _parse_eng_file(self, full_file_path):
        with open(full_file_path, "r") as file:
            lines = file.readlines()

        motor_name = None
        time_points = []
        thrust_points = []
        propellant_mass_kg = 0
        header_parsed = False

        for line in lines:
            line = line.strip()

            if not line or line.startswith(";"):
                continue

            if not header_parsed:
                header_bits = line.split()

                motor_name = header_bits[0].upper()
                propellant_mass_kg = float(header_bits[4])
                header_parsed = True
                continue

            data_bits = line.split()
            if len(data_bits) >= 2:
                time_points.append(float(data_bits[0]))
                thrust_points.append(float(data_bits[1]))

        if motor_name and len(time_points) > 0:
            burn_duration = time_points[-1]

            self.registry[motor_name] = {
                "time_points": time_points,
                "thrust_points": thrust_points,
                "propellant_kg": propellant_mass_kg,
                "burn_time": burn_duration
            }

if __name__ == "__main__":
    pipeline = AutomatedIngestionPipeline()
    pipeline.compile_motors()