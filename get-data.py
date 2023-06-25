import os
import psutil
import subprocess
import statistics
import time

def get_cpu_temperature():
    try:
        if psutil.WINDOWS:
            # Windows
            command = "wmic path Win32_PerfFormattedData_Counters_ThermalZoneInformation get Temperature /value"
            result = subprocess.check_output(command, shell=True, universal_newlines=True)
            temperature = [float(s.split('=')[1]) / 10.0 for s in result.strip().split('\n') if s.strip().startswith('Temperature')]
            if temperature:
                return max(temperature)
        else:
            # Linux
            thermal_dir = '/sys/class/thermal'
            for device in os.listdir(thermal_dir):
                if device.startswith('thermal_zone'):
                    temp_file = os.path.join(thermal_dir, device, 'temp')
                    with open(temp_file, 'r') as f:
                        temperature = float(f.read().strip()) / 1000.0
                        return temperature
    except Exception as e:
        print(f"Error getting CPU temperature: {e}")

    return None


def monitor_cpu_temperature(interval):
    temperatures = []
    start_time = time.time()

    while time.time() - start_time < interval:
        temperature = get_cpu_temperature()
        if temperature is not None:
            temperatures.append(temperature)
        time.sleep(1)

    if temperatures:
        min_temperature = min(temperatures)
        max_temperature = max(temperatures)
        avg_temperature = statistics.mean(temperatures)

        print(f"Maximum Temperature: {max_temperature} °C")
        print(f"Average Temperature: {avg_temperature} °C")
        print(f"Minimum Temperature: {min_temperature} °C")
    else:
        print("No temperature data available.")


# ---- START OF SCRIPT ----
if __name__ == '__main__':
    interval = 20
    utilization = 100 
    cpu_load_script_path = 'assets/loads/cpu-load.py' 

    cpu_load_process = subprocess.Popen(['python', cpu_load_script_path, str(interval), str(utilization)])
    monitor_cpu_temperature(interval)
    cpu_load_process.terminate()