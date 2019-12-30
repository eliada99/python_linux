#!/usr/bin/python
"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-5136306
"""
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class HostInterfaceEth:
    def __init__(self, host_linux_obj, int_name):
        interface_dic = self.collect_mlx_interfaces(int_name, host_linux_obj)
        self.interface_name = str(int_name)
        self.mtu = int(interface_dic['mtu'])
        self.mac_address = interface_dic['mac_address']
        self.speed = int(interface_dic['speed']) / 1000
        self.current_link_width = int(interface_dic['current_link_width'])
        self.mst_device = interface_dic['mst_device']
        self.pci = interface_dic['pci']
        self.driver_mlx = interface_dic['driver_mlx']
        self.connect_x = interface_dic['connect_x']
        self.fw_version = host_linux_obj.run_cmd("flint -d " + self.mst_device + " q | grep -i fw | grep -i version",
                                         r'FW\sVersion\:\s+(\d{2}\.\d{2}\.\d{4})', 1).rstrip("\n")

        self.ipv4 = interface_dic['IPADDR']
        self.ipv6 = interface_dic['IPV6ADDR']
        self.type = interface_dic['TYPE']

    # Getters methods
    def get_interface_name(self):
        return self.int_name

    def get_mst_device(self):
        return self.mst_device

    def get_fw_version(self):
        return self.fw

    def get_pci(self):
        return self.pci

    def get_driver_mlx(self):
        return self.driver_mlx

    def get_int_name(self):
        return self.int_name

    def get_connect_x(self):
        return self.connect_x

    def get_ipv4(self):
        return self.ipv4

    def get_ipv6(self):
        return self.ipv6

    def get_type(self):
        return self.type

    def collect_mlx_interfaces(self, interface, host_linux_obj):
        d = {'mtu': host_linux_obj.run_cmd("cat /sys/class/net/" + interface + "/mtu", 0, 1).rstrip("\n"),
             'mac_address': host_linux_obj.run_cmd("cat /sys/class/net/" + interface + "/address", 0, 1).rstrip("\n"),
             'speed': host_linux_obj.run_cmd("cat /sys/class/net/" + interface + "/speed", 0, 1).rstrip("\n"),
             'current_link_width': host_linux_obj.run_cmd("cat /sys/class/net/" + interface +"/device/current_link_width", 0, 1).rstrip("\n"),
             'mst_device': host_linux_obj.run_cmd("mst status -v | grep -i " + interface, r'.*(/dev/mst/mt.*\d)\s+\d{2}\:\d{2}\.\d.*', 1),
             'pci': host_linux_obj.run_cmd("mst status -v | grep -i " + interface, r'.*(\w{2}\:\d{2}\.\d).*', 1),
             'driver_mlx': host_linux_obj.run_cmd("mst status -v | grep -i " + interface, r'.*(mlx\d\_\d)\s+net-\w+\s+', 1),
             'connect_x': host_linux_obj.run_cmd("mst status -v | grep -i " + interface, r'(\w+\d?)\(rev:\d+\).*', 1)}
        conf_file_content = host_linux_obj.run_cmd("cat /etc/sysconfig/network-scripts/ifcfg-"+interface, 0,
                                                    1).split("\n")
        for att in conf_file_content:
            tmp = att.split("=")
            if 2 > len(tmp):
                continue
            d[tmp[0]] = tmp[1]

        return d

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)