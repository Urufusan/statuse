import os
import time


class CPU:
    @staticmethod
    def usage():
        with open("/proc/stat", "r") as stat_file:
            for line in stat_file:
                fields = line.split()
                if fields[0] == "cpu":
                    times = list(map(int, fields[1:]))
                    return 100 - times[3] * 100 / sum(times)

    @staticmethod
    def get_info():
        info = {"processors": 0}
        with open("/proc/cpuinfo", "r") as cpu_info_file:
            for line in cpu_info_file:
                # print("DEBUG", line)
                try:
                    key, val = map(str.strip, line.split(":"))
                except ValueError:
                    continue
                key = key.replace(" ", "_").lower()
                if key == "processor":
                    info["processors"] += 1
                else:
                    if val:
                        info[key] = val
        return info


class OS:
    @staticmethod
    def processes():
        return len([name for name in os.listdir("/proc") if name.isdigit()])

    @staticmethod
    def get_name():
        with open("/etc/os-release", "r") as os_release_file:
            for line in os_release_file:
                key, val = line.split("=")
                if key.strip() == "NAME":
                    return val.split('"')[1].strip()
        return "Unknown"
    
    # /sys/devices/virtual/dmi/id/product_family 

    @staticmethod
    def get_board():
        try:
            with open("/sys/devices/virtual/dmi/id/product_family", "r") as board_name:
                return board_name.read().strip()
        except:
            return "Unknown"

class Stats:
    @staticmethod
    def plaintext():
        os_name = OS.get_name()
        cpu_info = CPU.get_info()
        cpu_usage = CPU.usage()
        board_name = OS.get_board()
        return f"""OS: {os_name}
CPU: {cpu_info.get('model_name', 'Unknown')}
Model: {board_name}
Processors: {cpu_info.get('processors', 0)}
Processes: {OS.processes()}
CPU usage: {"{:.2f}".format(cpu_usage) if cpu_usage is not None else 'Unknown'}%
System time: {time.strftime("%Y-%m-%d %H:%M:%S")}"""


if __name__ == "__main__":
    # Example usage:
    print(Stats.plaintext())
