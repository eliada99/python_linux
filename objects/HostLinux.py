#!/usr/bin/python
from os import sys, path
import re
import subprocess

from modules import utilities
from RemoteConnection import RemoteConnection

VER_TOOLS_PATH = '/mswg/projects/ver_tools/reg2_latest/install.sh'
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class HostLinux:
    def __init__(self, host_ip):
        print ("------------------------------------------")
        utilities.reporter("Start to build host_linux object of host: " + host_ip, 'blue')
        self.last_output = None
        remote = RemoteConnection()
        conn = remote.connect(host_ip)
        self.conn = None if conn is None else conn
        self.machine_type = conn.modules.platform.system()  # Returns the system/OS name, e.g. 'Linux', 'Windows'
        self.processor_name = conn.modules.platform.processor()  # Returns the processor name, e.g. 'amdk6' / 'x86_64'
        self.hostname = conn.modules.platform.node()             # returns the host name, e. g 'bfhp12'
        self.os_details = conn.modules.platform.platform(aliased=0, terse=0) # 'Linux-3.10.0-693.el7.x86_64-x86_64-with-redhat-7.4-Maipo'
        self.linux_distribution = conn.modules.platform.linux_distribution()[0] # 'Red Hat Enterprise Linux Server'
        self.ip = host_ip

        dictionary_data = self.collect_host_data()
        self.ofed_info = dictionary_data['ofed_info']
        self.mst_version = dictionary_data['mst_version']
        self.mst_device = dictionary_data['mst_device']
        self.fw =   dictionary_data['fw']
        self.exp_rom = dictionary_data['exp_rom']
        self.pci = dictionary_data['pci']
        self.driver_mlx = dictionary_data['driver_mlx']
        self.connect_x = dictionary_data['connect_x']
        self.board_details = dictionary_data['board_details']
        self.part_number = dictionary_data['part_number']
        self.hca_pid = dictionary_data['hca_pid']
        print self

    # Getters methods
    def get_conn(self):
        return self.conn

    def get_ip(self):
        return self.ip

    def get_machine_type(self):
        return self.machine_type

    def get_processor_name(self):
        return self.processor_name

    def get_os_details(self):
        return self.os_details

    def get_linux_distribution(self):
        return self.linux_distribution

    def get_hostname(self):
        return self.hostname

    def get_last_output(self):
        return self.last_output

    def get_ofed_info(self):
        return self.ofed_info

    def get_mst_version(self):
        return self.mst_version

    def get_mst_device(self):
        return self.mst_device

    def get_fw(self):
        return self.fw

    def get_exp_rom(self):
        return self.exp_rom

    def get_pci(self):
        return self.pci

    def get_driver_mlx(self):
        return self.driver_mlx

    def get_connect_x(self):
        return self.connect_x

    def get_board_details(self):
        return self.board_details

    def get_part_number(self):
        return self.part_number

    def get_hca_pid(self):
        return self.hca_pid

    # Setters methods
    def set_last_output(self, last_output):
        self.last_output = last_output

    # run command def
    # with/without regex to pull only the needed output
    # with/without return value
    def run_cmd(self, cmd, reg, return_value=0, timeout=60):
        if hasattr(self, 'hostname'):
            host = self.get_hostname()
        else:
            host = "No Name Yet"
        utilities.reporter("Function: HostLinux.run_cmd, Object: HostLinux: " + host + "\nCommand: " + cmd + "\n",
                           'green')
        proc = self.conn.modules.subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                  universal_newlines=True)
        stdout, stderr = proc.communicate()

        if stderr:
            utilities.reporter("Something went wrong: " + stderr, 'red')
            self.last_output = stderr  # need to verify it
            raise Exception("failed in command: " + cmd)
            return None
        utilities.reporter("Output of command is: " + stdout, 'blue')
        self.set_last_output(stdout)
        if reg:
            try:
                stdout = re.findall(reg, stdout)[0]
            except:
                utilities.reporter("Host: " + self.get_hostname() + "Command Fail: " + cmd + "\n" + stdout, 'red')
                return None
        # if cmdStatus: return None
        if return_value: return stdout

    def collect_host_data(self):
        if not self.run_cmd("mst start", 0, 1):
            utilities.reporter("Fail to start the driver: \"mst start\"", 'red')
            return None
        d = {}
        d['ofed_info'] = self.run_cmd("ofed_info -s", r'\w+\-(\d\.\d\-\d\.\d\.\d+\.\d)', 1)
        d['mst_version'] = self.run_cmd("mst version", r'mst\W+mft\s(\d\.\d+\.\d\-\d+).*', 1)
        d['mst_device'] = self.run_cmd("mst status -v", r'\W+(/dev/mst/mt\d+\_\w+\d).*', 1)
        mstDevice = d['mst_device'].lstrip()
        d['fw'] = self.run_cmd("flint -d " + mstDevice + " q | grep -i fw | grep -i version",
                               r'FW\sVersion\:\s+(\d{2}\.\d{2}\.\d{4})', 1)
        d['exp_rom'] = self.run_cmd("flint -d " + mstDevice + " q | grep -i rom", r'Rom\sInfo\:\s+(.*)', 1)
        d['pci'] = self.run_cmd("lspci | grep -i mellanox", r'^(\w{2}\:\d{2}\.\d).*', 1)
        d['driver_mlx'] = self.run_cmd("mst status -v | grep -i " + mstDevice, r'.*(mlx\d\_0)\s+net-\w+\s+', 1)
        d['connect_x'] = self.run_cmd("mst status -v | grep -i " + mstDevice, r'(\w+\d?)\(rev:\d+\).*', 1)
        d['board_details'] = self.run_cmd('mlxburn -d ' + mstDevice + ' -vpd', r'.*Board\sId\s+(.*)', 1)
        d['part_number'] = self.run_cmd('mlxburn -d ' + mstDevice + ' -vpd', r'.*Part\sNumber\s+(\w+-\w+)\s+.*', 1)
        d['hca_pid'] = self.run_cmd('flint -d ' + mstDevice + ' q', r'.*PSID:\s+(.*)', 1)
        return d

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
