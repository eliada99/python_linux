#!/usr/bin/python
"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-5136306
"""
from os import sys, path

from modules import utilities
from objects.host.Host import Host

VER_TOOLS_PATH = '/mswg/projects/ver_tools/reg2_latest/install.sh'
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class HostLinux(Host):
    def __init__(self, host_ip):
        Host.__init__(self, host_ip)
        dictionary_data = self.collect_host_data()
        self.ofed_info = dictionary_data['ofed_info']
        self.mst_version = dictionary_data['mst_version']
        self.mst_device = dictionary_data['mst_device']
        self.exp_rom = dictionary_data['exp_rom']
        self.pci = dictionary_data['pci']
        self.driver_mlx = dictionary_data['driver_mlx']
        self.connect_x = dictionary_data['connect_x']
        self.board_details = dictionary_data['board_details']
        self.part_number = dictionary_data['part_number']
        self.hca_pid = dictionary_data['hca_pid']
        self.uname = dictionary_data['uname']

    # Getters methods
    def get_ofed_info(self):
        return self.ofed_info

    def get_mst_version(self):
        return self.mst_version

    def get_mst_device(self):
        return self.mst_device

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

    # function: collect_host_data
    # run commands on your host via RPyC to pull the setup details
    def collect_host_data(self):
        if not self.run_cmd("mst start", 0, 1):
            utilities.reporter("Fail to start the driver: \"mst start\"", 'red')
            return None
        d = {'mst_device': self.run_cmd("mst status -v", r'\W+(/dev/mst/mt\d+\_\w+\d).*', 1)}
        mst_device = d['mst_device'].lstrip()
        d['ofed_info'] = self.run_cmd("ofed_info -s", r'\w+\-(\d\.\d\-\d\.\d\.\d+\.\d)', 1)
        d['mst_version'] = self.run_cmd("mst version", r'mst\W+mft\s(\d\.\d+\.\d\-\d+).*', 1)
        d['exp_rom'] = self.run_cmd("flint -d " + mst_device + " q | grep -i rom", r'Rom\sInfo\:\s+(.*)', 1)
        d['pci'] = self.run_cmd("lspci | grep -i mellanox", r'^(\w{2}\:\d{2}\.\d).*', 1)
        d['driver_mlx'] = self.run_cmd("mst status -v | grep -i " + mst_device, r'.*(mlx\d\_0)\s+net-\w+\s+', 1)
        d['connect_x'] = self.run_cmd("mst status -v | grep -i " + mst_device, r'(\w+\d?)\(rev:\d+\).*', 1)
        d['board_details'] = self.run_cmd('mlxburn -d ' + mst_device + ' -vpd', r'.*Board\sId\s+(.*)', 1)
        d['part_number'] = self.run_cmd('mlxburn -d ' + mst_device + ' -vpd', r'.*Part\sNumber\s+(\w+-\w+)\s+.*', 1)
        d['hca_pid'] = self.run_cmd('flint -d ' + mst_device + ' q', r'.*PSID:\s+(.*)', 1)
        d['uname'] = self.run_cmd('uname -a', 0, 1)
        return d

    # print object details
    def print_me(self):
        print ("------ Class " + self.__class__.__name__ + ": ------")
        return "-------------------------------\n"\
               "Hostname:    " + self.hostname + "\n" \
               "IP:          " + self.ip + "\n" \
               "Ofed - info: " + self.ofed_info + "\n" \
               "MST Version: " + self.mst_version + " \n" \
               "MST Device:  " + self.mst_device + "\n" \
               "Pci:         " + self.pci + "\n" \
               "Driver MLX:  " + self.driver_mlx + "\n" \
               "ConnectX:    " + self.connect_x + "\n" \
               "Board:       " + self.board_details + "\n" \
               "Part_number: " + self.part_number + "\n" \
               "HCA_pid:     " + self.hca_pid + "\n" \
               "Machine:     " + self.machine_type + "\n" \
               "Proc - name: " + self.processor_name + "\n" \
               "OS_details:  " + self.os_details + "\n" \
               "Linux_dis:   " + self.linux_distribution + "\n" \
               "uname:       " + self.uname + \
               "-------------------------------"

