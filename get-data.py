import os
import psutil
import subprocess
import statistics
import time
import cpuinfo
import platform
import GPUtil
from datetime import datetime


#---------------------------------------------------------#
#                                                         #
# ------------------ CONSOLE OUTPUT COLORS ---------------#
#                                                         #
#---------------------------------------------------------#
def prError(skk):print("\033[91m {}\033[00m" .format(skk))
def prOk(skk):print("\033[92m {}\033[00m" .format(skk))
def prWarning(skk):print("\033[93m {}\033[00m" .format(skk))
def prInfo(skk):print("\033[94m {}\033[00m" .format(skk))

#---------------------------------------------------------#
#                                                         #                            
# ------------------ GENERAL SYSTEM INFO -----------------#
#                                                         #
#---------------------------------------------------------#

def getSystemSpecs():
    specs = {}
    prInfo("[INFO] - Retrieving system specifications")

    # Retrieve RAM information
    ram = psutil.virtual_memory()
    total_ram = ram.total // (1024 * 1024)
    specs["Total RAM"] = total_ram

    # Retrieve CPU information
    cpu_info = cpuinfo.get_cpu_info()
    cpu_name = cpu_info["brand_raw"]
    cpu_architecture = platform.machine()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_max_freq = psutil.cpu_freq().max
    cpu_base_freq = psutil.cpu_freq().min
    specs["CPU"] = cpu_name
    specs["CPU Architecture"] = cpu_architecture
    specs["CPU Cores"] = cpu_cores
    specs["CPU Threads"] = cpu_threads
    specs["Max CPU Frequency"] = cpu_max_freq
    specs["Base CPU Frequency"] = cpu_base_freq

    network_cards = psutil.net_if_addrs()
    network_card_list = []
    for interface_name, interface_addresses in network_cards.items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                network_card_list.append(interface_name)
    specs["Network Cards"] = network_card_list

    gpus = GPUtil.getGPUs()
    gpu_list = []
    for gpu in gpus:
        gpu_list.append(gpu.name)
    specs["GPU Names"] = gpu_list
    prOk("[OK] - System specifications retrieved")

    return specs


def get_battery_status():
    battery = psutil.sensors_battery()
    prInfo("[INFO] - Retrieving battery status")
    if battery is not None:
        plugged = battery.power_plugged
        percent = battery.percent
        remaining = battery.secsleft
        power_status = "Plugged in" if plugged else "Not plugged in"
        
        if plugged:
            time_remaining = "Charging"
        else:
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            time_remaining = f"{hours} hours {minutes} minutes"
        
        prOk("[OK] - Battery status retrieved")
        return {
            'percentage': percent,
            'power_status': power_status,
            'time_remaining': time_remaining,
        }
    else:
        prError("[ERROR] - No battery information available.")
        return None



def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append({
            'pid': proc.pid,
            'name': proc.name(),
            'cpu_percent': proc.cpu_percent(),
            'memory_percent': proc.memory_percent()
        })
    # Sort processes by CPU percent in descending order
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes


#---------------------------------------------------------#
#                                                         #                            
# ------------------- GENERATING REPORT ------------------#
#                                                         #
#---------------------------------------------------------#

def createProcessesTable():
    running_processes = get_running_processes()
    total_processes = len(running_processes)

    table_rows = ''
    for process in running_processes:
        table_rows += f"""
        <tr>
            <td>{process['pid']}</td>
            <td>{process['name']}</td>
            <td>{process['cpu_percent']}</td>
            <td>{process['memory_percent']}</td>
        </tr>"""

    html = f"""
<div class="container">
    <h1 id="systemproc">Running system processes</h1>
    <p>Total processes: {total_processes}</p>
    <table>
        <tr>
            <th>PID</th>
            <th>Process name</th>
            <th>CPU percent</th>
            <th>Memory percent</th>
        </tr>
        {table_rows}
    </table>
</div>
    """
    return html


def printResults(min_temperature, max_temperature, avg_temperature, interval, idle_temperature):
    processesTable = createProcessesTable()
    batteryStatus = get_battery_status()
    systemSpecs = getSystemSpecs()
    now = datetime.now()
    time = now.strftime("%Y-%m-%d-%H-%M-%S")
    template = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report from - {time}</title>
    <style>
        body {{
            background-color: #222;
            color: #fff;
            font-family: Arial, sans-serif;
        }}

        h1 {{
            color: #fff;
        }}

        p {{
            color: #ccc;
        }}

        ul {{
            list-style-type: none;
            background-color: #333;
            padding: 10px;
            margin: 0;
            display: flex;
            justify-content: space-around;
        }}

        li {{
            display: inline-block;
            margin-right: 20px;
        }}

        a {{
            color: #fff;
            text-decoration: none;
        }}

        .container {{
            margin: 20px;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }}

        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}

        th {{
            background-color: #333;
            color: #fff;
        }}

        .dark-mode {{
            background-color: #222;
            color: #fff;
        }}
    </style>
</head>

<body class="dark-mode">
    <ul>
        <li><a href="#systemspec">System specifications</a></li>
        <li><a href="#battery">Battery status</a></li>
        <li><a href="#benchmark">CPU benchmark results</a></li>
        <li><a href="#systemproc">Running system processes</a></li>
    </ul>
    <div class="container">
        <h1 id="systemspec">System specifications</h1>
        <p>CPU: {systemSpecs['CPU']} <br>CPU Architecture: {systemSpecs['CPU Architecture']} <br>CPU Cores: {systemSpecs['CPU Cores']} <br>CPU Threads: {systemSpecs['CPU Threads']} <br>Max CPU Frequency: {systemSpecs['Max CPU Frequency']} <br>Base CPU Frequency: {systemSpecs['Base CPU Frequency']} <br>GPU Names: {systemSpecs['GPU Names']} <br>Network Cards: {systemSpecs['Network Cards']} <br>Total RAM: {systemSpecs['Total RAM']}MB </p>
    </div>
    <hr>
    <div class="container">
        <h1 id="battery">Battery status</h1>
        <p>Percentage: {batteryStatus['percentage']}% <br>Power status: {batteryStatus['power_status']} <br>Time remaining: {batteryStatus['time_remaining']} </p>
    </div>
    <hr>
    <div class="container">
        <h1 id="benchmark">Benchmark results</h1>
        <p>Benchmark duration: {interval}sec <br>Maximum CPU temperature: {max_temperature}°C <br>Average CPU temperature: {avg_temperature}°C <br>Minimum CPU temperature: {min_temperature}°C </p>
    </div>
    <hr>
    {processesTable}
</body>

</html>
"""

    write = open(time+".html", "w")
    write.write(template)
    write.close()
    prOk(f"[OK] - HTML report generated: {time}.html")



#---------------------------------------------------------#
#                                                         #                            
# ------------------- SYSTEM BENCHMARK -------------------#
#                                                         #
#---------------------------------------------------------#

def get_cpu_temperature():
    try:
        prInfo("[INFO] - Retrieving CPU temperature")
        if psutil.WINDOWS:
            # Windows
            command = "wmic path Win32_PerfFormattedData_Counters_ThermalZoneInformation get Temperature /value"
            result = subprocess.check_output(command, shell=True, universal_newlines=True)
            temperature = [float(s.split('=')[1]) / 10.0 for s in result.strip().split('\n') if s.strip().startswith('Temperature')]
            if temperature:
                prOk(f"[OK] - CPU temperature: {temperature[0]}°C")
                return max(temperature)
        else:
            # Linux
            thermal_dir = '/sys/class/thermal'
            for device in os.listdir(thermal_dir):
                if device.startswith('thermal_zone'):
                    temp_file = os.path.join(thermal_dir, device, 'temp')
                    with open(temp_file, 'r') as f:
                        temperature = float(f.read().strip()) / 1000.0
                        prOk(f"[OK] - CPU temperature: {temperature}°C")
                        return temperature
    except Exception as e:
        prError(f"[ERROR] - getting CPU temperature: {e}")

    return None


def monitor_cpu_temperature(interval, utilization):
    idle_temperature = get_cpu_temperature()
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
        printResults(min_temperature, max_temperature, avg_temperature, interval, idle_temperature)
    else:
        print("No temperature data available.")


if __name__ == '__main__':
    interval = 0
    utilization = 0 
    userinput = input("Would you like to customize the benchmark? [y/n] ")
    if userinput == "n":
        prInfo("[INFO] - Using default values...")
        interval = 120
        utilization = 100
    else:
        interval = int(input("Enter the benchmark duration in seconds: "))
        utilization = int(input("Enter the CPU utilization in percentage: "))

    prWarning(f"[WARNING] - For the best results, please stay focussed on this window during the test. The program will start in 5 seconds.")
    time.sleep(5)
    cpu_load_script_path = 'assets/loads/cpu-load.py' 

    cpu_load_process = subprocess.Popen(['python', cpu_load_script_path, str(interval), str(utilization)])
    monitor_cpu_temperature(interval, utilization)
    cpu_load_process.terminate()