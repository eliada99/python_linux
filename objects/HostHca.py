#!/usr/bin/python
from os import sys, path
from modules import utilities

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class HostHca:
    def __init__(self, host_linux_obj, serverInterfaceEth1, serverInterfaceEth2):
        self.mst_device = host_linux_obj.run_cmd("mst status -v", r'\W+(/dev/mst/mt\d+\_\w+\d).*', 1)
        mstDevice = serverInterfaceEth1.get_mst_device().lstrip()
        cmd = "flint -d " + mstDevice + " q | grep -i fw | grep -i version"
        self.fw = host_linux_obj.run_cmd(cmd, r'FW\sVersion\:\s+(\d{2}\.\d{2}\.\d{4})', 1)
        self.exp_rom = host_linux_obj.run_cmd("flint -d " + mstDevice + " q | grep -i rom", r'Rom\sInfo\:\s+(.*)', 1)
        self.pci = serverInterfaceEth1.get_pci()
        self.part_number = host_linux_obj.run_cmd('mlxburn -d ' + mstDevice + ' -vpd',
                                                  r'.*Part\sNumber\s+(\w+-\w+)\s+.*', 1)
        self.hca_pid = host_linux_obj.run_cmd('flint -d ' + mstDevice + ' q', r'.*PSID:\s+(.*)', 1)
        self.interface_1_object = serverInterfaceEth1
        self.interface_2_object = serverInterfaceEth2

    # Getters methods

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

    def get_int_name(self):
        return self.int_name

    def get_connect_x(self):
        return self.connect_x

    def get_board_id(self):
        return self.board_id

    def get_part_number(self):
        return self.part_number

    def get_hca_pid(self):
        return self.hca_pid

    # Setters methods

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)