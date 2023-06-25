import os
import psutil
import subprocess
import statistics
import time
from datetime import datetime

def prError(skk):print("\033[91m {}\033[00m" .format(skk))
def prOk(skk):print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk):print("\033[93m {}\033[00m" .format(skk))
def prInfo(skk):print("\033[94m {}\033[00m" .format(skk))


def printResults(min_temperature, max_temperature, avg_temperature, interval):
    now = datetime.now()
    time = now.strftime("%Y-%m-%d-%H-%M-%S")
    template = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PC Benchmark</title>
</head>

<body>
    <h1>Benchmark results:</h1>
    <p>Benchmark duration: {interval}sec <br>Maximum CPU temperature: {max_temperature}°C <br>Average CPU temperature: {avg_temperature}°C <br>Minimum CPU temperature: {min_temperature}°C </p>
</body>

</html>
    """

    write = open(time+".html", "w")
    write.write(template)
    write.close()
    prOk(f"[OK] - HTML report generated: {time}.html")


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


def monitor_cpu_temperature(interval, utilization):
    temperatures = []
    start_time = time.time()
    prInfo(f"[INFO] - Starting benchmark for {interval} seconds and CPU utilization of {utilization}%")

    while time.time() - start_time < interval:
        temperature = get_cpu_temperature()
        if temperature is not None:
            temperatures.append(temperature)
        time.sleep(1)

    if temperatures:
        min_temperature = min(temperatures)
        max_temperature = max(temperatures)
        avg_temperature = statistics.mean(temperatures)

        prOk(f"[OK] - CPU test finished.")
        prInfo("[INFO] - Generating HTML report...")
        printResults(min_temperature, max_temperature, avg_temperature, interval)
    else:
        print("No temperature data available.")


if __name__ == '__main__':
    interval = 0
    utilization = 0 
    userinput = input("Would you like to customize the benchmark? [y/n]")
    if userinput == "n":
        prInfo("[INFO] - Using default values...")
        interval = 120
        utilization = 100
    else:
        interval = int(input("Enter the benchmark duration in seconds: "))
        utilization = int(input("Enter the CPU utilization in percentage: "))


    cpu_load_script_path = 'assets/loads/cpu-load.py' 

    cpu_load_process = subprocess.Popen(['python', cpu_load_script_path, str(interval), str(utilization)])
    monitor_cpu_temperature(interval, utilization)
    cpu_load_process.terminate()