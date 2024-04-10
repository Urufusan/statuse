# Copyright (C) 2024 Urufusan
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import time
import platform
import psutil


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
        _base_board_name = ""
        try:
            with open("/sys/devices/virtual/dmi/id/sys_vendor", "r") as board_name:
                _base_board_name += board_name.read().strip()
            with open("/sys/devices/virtual/dmi/id/product_family", "r") as board_name:
                _base_board_name += " " + board_name.read().strip()
            with open("/sys/devices/virtual/dmi/id/product_name", "r") as board_name:
                _base_board_name += " " + board_name.read().strip()
            return _base_board_name
        except:
            return "Unknown"

class Stats:
    @staticmethod
    def plaintext():
        os_name = OS.get_name()
        cpu_info = CPU.get_info()
        cpu_usage = CPU.usage()
        board_name = OS.get_board()
        ram_data = (round(psutil.virtual_memory().total / (1024 ** 3), 2), round(psutil.virtual_memory().used / (1024 ** 3), 2))
        return f"""Hostname: {platform.node()}
OS: {os_name} {platform.release()}
CPU: {cpu_info.get('model_name', 'Unknown')} ({platform.machine()})
Model: {board_name}
Processors: {cpu_info.get('processors', 0)}
Processes: {OS.processes()}
CPU usage: {"{:.2f}".format(cpu_usage) if cpu_usage is not None else 'Unknown'}%
RAM usage: {ram_data[1]}GB / {ram_data[0]}GB ({int((ram_data[1]/ram_data[0])*100)}%)
System time: {time.strftime("%Y-%m-%d %H:%M:%S")}"""


if __name__ == "__main__":
    # Example usage:
    print(Stats.plaintext())
