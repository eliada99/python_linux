#!/usr/bin/python
from os import sys, path
import hwinfo

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class HostHca:
    def __init__(self, host_linux_obj, server_interface_eth1, server_interface_eth2):
        d = self.collect_hca_data(host_linux_obj, server_interface_eth1)
        self.mst_device = d['mst_device']
        self.fw_version = d['fw_version']
        self.exp_rom = d['exp_rom']
        self.pci = d['pci']
        self.part_number = d['part_number']
        self.hca_pid = d['hca_pid']
        self.driver = d['driver']
        self.interface_1_obj = server_interface_eth1
        self.interface_2_obj = server_interface_eth2

    # Getters methods
    def get_mst_device(self):
        return self.mst_device

    def get_fw_version(self):
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

    def collect_hca_data(self, host_linux_obj, server_interface_eth1):
        mst_device = server_interface_eth1.get_mst_device().lstrip()

        d = {}
        d['mst_device'] = mst_device
        d['fw_version'] = host_linux_obj.run_cmd("flint -d " + mst_device + " q | grep -i fw | grep -i version",
                                                 r'FW\sVersion\:\s+(\d{2}\.\d{2}\.\d{4})', 1).lstrip()
        d['exp_rom'] = host_linux_obj.run_cmd("flint -d " + d['mst_device'] + " q | grep -i rom", r'Rom\sInfo\:\s+(.*)',
                                              1).lstrip()
        d['pci'] = server_interface_eth1.get_pci()
        d['part_number'] = host_linux_obj.run_cmd('mlxburn -d ' + d['mst_device'] + ' -vpd',
                                                  r'.*Part\sNumber\s+(\w+-\w+)\s+.*', 1).lstrip()
        d['hca_pid'] = host_linux_obj.run_cmd('flint -d ' + d['mst_device'] + ' q', r'.*PSID:\s+(.*)', 1).lstrip()
        d['driver'] = server_interface_eth1.get_driver_mlx()
        return d

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)