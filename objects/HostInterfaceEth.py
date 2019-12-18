#!/usr/bin/python
from os import sys, path
from modules import utilities

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class HostInterfaceEth:
    def __init__(self, host_linux_obj, int_name):
        self.int_name   = int_name
        self.mst_device = host_linux_obj.run_cmd("mst status -v | grep -i "+int_name,
                                                 r'.*(/dev/mst/mt.*\d)\s+\d{2}\:\d{2}\.\d.*', 1)
        mstDevice = self.mst_device
        self.fw   = host_linux_obj.run_cmd("flint -d " + mstDevice + " q | grep -i fw | grep -i version",
                                                                 r'FW\sVersion\:\s+(\d{2}\.\d{2}\.\d{4})', 1)
        self.pci        = host_linux_obj.run_cmd("mst status -v | grep -i " + int_name, r'.*(\w{2}\:\d{2}\.\d).*', 1)
        self.driver_mlx = host_linux_obj.run_cmd("mst status -v | grep -i " + int_name, r'.*(mlx\d\_\d)\s+net-\w+\s+', 1)
        self.connect_x  = host_linux_obj.run_cmd("mst status -v | grep -i " + int_name, r'(\w+\d?)\(rev:\d+\).*', 1)

    # Getters methods
    def get_interface_name(self):
        return self.int_name

    def get_mst_device(self):
        return self.mst_device

    def get_fw(self):
        return self.fw

    def get_pci(self):
        return self.pci

    def get_driver_mlx(self):
        return self.driver_mlx

    def get_int_name(self):
        return self.int_name

    def get_connect_x(self):
        return self.connect_x

    # Setters methods

    # print object attributes
    def print_content(self):
        utilities.reporter("Printing the attributes of Host_linux Object:", 'bold')
        try:
            print ("Host Name:     " + self.get_ip() + "\n" +
                   "MST Device:    " + self.get_mst_device() + "\n" +
                   "FW Version:    " + self.get_fw() + "\n" +
                   "PCI:           " + self.get_pci() + "\n" +
                   "------------------------------------------\n")
        except:
            print("Fail to print the object attributes!\n" +
                  "------------------------------------------\n")
