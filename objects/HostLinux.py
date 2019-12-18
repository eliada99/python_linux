#!/usr/bin/python
from os import sys, path
import re
import rpyc
import subprocess

from modules import sshParamiko, utilities

VER_TOOLS_PATH = '/mswg/projects/ver_tools/reg2_latest/install.sh'
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class HostLinux:
    def __init__(self, host_ip):
        print ("------------------------------------------")
        utilities.reporter("Start to build host_linux object of host: " + host_ip, 'blue')
        self.last_output = None
        conn = self.reconnect_to_host(host_ip)
        self.conn = None if conn is None else conn

        if not self.run_cmd("mst start", 0, 1):
            utilities.reporter("Fail to start the driver: \"mst start\"", 'red')
            return None


        self.ip            = host_ip
        self.hostname      = self.run_cmd("hostname", 0, 1)
        self.ofed_info     = self.run_cmd("ofed_info -s", r'\w+\-(\d\.\d\-\d\.\d\.\d+\.\d)', 1)
        self.mst_version   = self.run_cmd("mst version", r'mst\W+mft\s(\d\.\d+\.\d\-\d+).*', 1)
        self.mst_device    = self.run_cmd("mst status -v", r'\W+(/dev/mst/mt\d+\_\w+\d).*', 1)
        mstDevice          = self.get_mst_device().lstrip()
        self.fw            = self.run_cmd("flint -d " + mstDevice + " q | grep -i fw | grep -i version",
                                           r'FW\sVersion\:\s+(\d{2}\.\d{2}\.\d{4})', 1)
        self.exp_rom       = self.run_cmd("flint -d " + mstDevice + " q | grep -i rom", r'Rom\sInfo\:\s+(.*)', 1)
        self.pci           = self.run_cmd("lspci | grep -i mellanox", r'^(\w{2}\:\d{2}\.\d).*', 1)
        self.driver_mlx    = self.run_cmd("mst status -v | grep -i " + mstDevice, r'.*(mlx\d\_0)\s+net-\w+\s+', 1)
        self.connect_x     = self.run_cmd("mst status -v | grep -i " + mstDevice, r'(\w+\d?)\(rev:\d+\).*', 1)
        self.board_details = self.run_cmd('mlxburn -d ' + mstDevice + ' -vpd', r'.*Board\sId\s+(.*)', 1)
        self.part_number   = self.run_cmd('mlxburn -d ' + mstDevice + ' -vpd', r'.*Part\sNumber\s+(\w+-\w+)\s+.*', 1)
        self.hca_pid       = self.run_cmd('flint -d ' + mstDevice + ' q', r'.*PSID:\s+(.*)', 1)

    # Getters methods
    def get_conn(self):
        return self.conn

    def get_ip(self):
        return self.ip

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

    # connect/reconnect to your host
    def reconnect_to_host(self, ip):
        var = None
        try:
            conn = rpyc.classic.connect(ip)
            return conn
        except:
            if not var:
                var = sshParamiko.ssh_command(str(ip), VER_TOOLS_PATH)
                self.reconnect_to_host(ip)   # --> a little bit dangerous .... ???!
            utilities.reporter("No connection to host: " + self.get_ip() + "!", 'red')
            return None

    # run command RPyC:
    # In
    # with/without regex to pull only the needed output
    # with/without return value
    def run_cmd(self, cmd, reg, return_value=0, timeout=60):
        if hasattr(self, 'hostname'): host = self.get_hostname()
        else:                         host = "No Name Yet"
        utilities.reporter("Function: HostLinux.run_cmd, Object: HostLinux: " + host + "\nCommand: " + cmd + "\n", 'green')
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
        #if cmdStatus: return None
        if return_value: return stdout

    # print object attributes
    def print_content(self):
        utilities.reporter("Printing the attributes of Host_linux Object:", 'bold')
        try:
            print ("Host Name:     " + self.get_ip() + "\n" +
                   "Ofed Info:     " + self.get_ofed_info() + "\n" +
                   "MST Version:   " + self.get_mst_version() + "\n" +
                   "MST Device:    " + self.get_mst_device() + "\n" +
                   "FW Version:    " + self.get_fw() + "\n" +
                   "Rom Info:      " + self.get_exp_rom() + "\n" +
                   "PCI:           " + self.get_pci() + "\n" +
                   "Board Id:      " + self.get_board_id() + "\n" +
                   "Part Number:   " + self.get_part_number() + "\n" +
                   "PSID:          " + self.get_psid() + "\n" +
                   "------------------------------------------\n")
        except:
            print("Fail to print the object attributes!\n" +
                  "------------------------------------------\n")