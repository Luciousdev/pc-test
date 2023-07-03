# System benchmark

## Table of contents

- [Info](#info)
    - [Support](#support)
    - [Packages](#packages) 
    - [What it does](#what-it-does) 
- [Guides](#guides)
    - [Manual guide](#manual-install-guide)
    - [Automatic install guide](#auto-install)
        - [Windows install](#windows-install)
        - [Linux install](#linux-install)
    - [How to use the program and default settings](#how-to-use-the-program&default-settings)
- [Output](#output)
- [Known-issues](#issues)
- [Made by](#made-by)

## Info

### Support

| OS | Support |
|---|---|
| Windows 10/11 | ⚠️ * |
| Manjaro/Arch | ✅ |
| Ubuntu/Debian | ✅ |
| MacOS | 🚧 ** |

\* CPU temperatures do work on windows, but on some devices it will report as 0. (currently working on a solution.)

\** State of MacOS is currently unknown, looking for people to test it. If you have a Mac and want to contribute, shoot me a message on [discord](https://discord.com/users/524229083014365194)

Note: You can find more issues under the [Known-issues](#issues) tab.

### Packages

List of all packages:
| Name | Version |
|---|---|
| psutil | 5.9.5 |
| py-cpuinfo | 9.0.0 |
| matplotlib | 3.7.1 |
| GPUtil | 1.4.0 |

These packages can be easily installed with pip. (look at the install guid for more details.)

### What-it-does

This script will gather basic data about the system and will run a small CPU benchmark to measure the temperatures. (More details can be found under the "Output" section.)

## Guides

### Manual-Install-guide

Install at least python 3.10 or above. Versions below that will most likely work but those haven't been tested and thus aren't fully supported.

1. Download/git clone the repository. (You can also get the versions from the [RELEASES](https://github.com/Luciousdev/pc-test/releases) tab)
2. pip install the requirements (Make sure your terminal session is in the downloaded folder.):
    ```
    pip install -r requirements.txt
    ```
3. Then you should be able to run the code with this command:
   ```
   python get-data.py
   ```

### Auto-install

#### Windows-install

For the windows install run the install-windows.bat file in the project repository.
The script will install python version 3.10 and run the project. If you already have the correct python version and just want to run the script use this command:

```
python get-data.py
```

#### Linux-install

To run the linux installer open a terminal and cd into the directory where you've downloaded the project.
Use this command to then run the script:

```
sh install-linux.sh
```

The script will install python version 3.10 and run the project. If you already have the correct python version and just want to run the script use this command:

```
python get-data.py
```

### How-to-use-the-program&default-settings

To use the script you can launch it with this command:
```
python get-data.py
```
When launching the program it will prompt you on if you'd like to customize the benchmark. The settings it will ask you to change are the CPU utilization (in %) and the total run time (in seconds).
These are the default settings:

| Run time  | CPU utilization  | Drop off time |
|---|---|---|
| 120 Seconds | 100%  | 60 Seconds |

#### Output

Small list of the output it will generate for you:
    - Benchmark results. (CPU temperature max, avg, min)
    - CPU drop off temperature after benchmark in a graph.
    - Battery status.
    - Basic specification about hte system.
    - List all and total running processes with the CPU usage and RAM usage. 
    - System info.
    - When the report is generated.
    
There are example reports for [WINDOWS](https://examples.luciousdev.nl/windows/) and for [LINUX](https://examples.luciousdev.nl/linux/), if you're interested in seeing the results before using the program.

## issues

- Temperature readings on windows do work but on some devices it will report as 0. (currently working on a fix.)
- Temperature readings on linux can be a bit buggy.
- CPU Percent readings are still a hit or miss.

## Made-by

This was made with love by [Lucy Puyenbroek (Luciousdev)](https://github.com/Luciousdev)
