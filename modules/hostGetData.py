#!/usr/bin/python

from os.path import abspath, exists
import re

'''
### The function return dictionary with the content of your 'versions.txt" file ###
input: file path
return value example:
dic["bfbImage"] = /auto/mswg/release/sw_mc_soc/CentOS7.5-4.20/CentOS7.5-4.20-MLNX_OFED_LINUX-UPSTREAM-LIBS-4.7-3.2.7.0.1-aarch64.bfb
dic["driver"]   = build=MLNX_OFED_LINUX-4.7-3.2.7.0  /.autodirect/mswg/release/MLNX_OFED/mlnx_ofed_install --with-rshim
dic["fw"]       = 18_26_4010
'''


def get_versions_from_file(path):
    f_path = abspath(path)
    if exists(f_path):
        with open(f_path) as f:
            content = f.read()
            f.close()

    dicVersions = {"bfbImage": re.findall('BFB: (.*)', content)[0], "driver": re.findall('MLNX_OFED: (.*)', content)[0],
           "fw": re.findall('FW: (.*)', content)[0]}

    return dicVersions
