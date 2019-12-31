#!/usr/bin/python

from modules import hostGetData
from modules import hostSetData
import globals
from modules import benchmark
from modules import utilities

VERSIONS_PATH = "../versions.txt"


def update_setup_bluefield(Obj):
    myRemoteLocal = globals.hostLinuxServer
    myRemoteLocal = globals.hostLinuxClient
    verDic = hostGetData.get_versions_from_file(VERSIONS_PATH)
    pass
    return
    #remoteObj.run_cmd()


def ping_test_ipv4():
    msg = ''
    if (benchmark.run_ping(globals.hostLinuxClient, globals.serverInterfaceEth1,
                 globals.clientInterfaceEth1, "ipv4") is None):
        noPingIpv4Port_1 = 1
        msg += ' ping fail from 1st port in IPv4'
    if (benchmark.run_ping(globals.hostLinuxClient, globals.serverInterfaceEth2,
                 globals.clientInterfaceEth2, "ipv4") is None):
        noPingIpv4Port_2 = 1
        msg += ' ping fail from 2nd port in IPv4'
    if msg:
        utilities.reporter(msg, 'red')
        return False
    return True


def ping_test_ipv6():
    msg = ''
    if (benchmark.run_ping(globals.hostLinuxClient, globals.serverInterfaceEth1,
                 globals.clientInterfaceEth1, "ipv6") is None):
        msg += ' ping fail from 1st port in IPv6'
    if (benchmark.run_ping(globals.hostLinuxClient, globals.serverInterfaceEth2,
                 globals.clientInterfaceEth2, "ipv6") is None):
        msg += ' ping fail from 2nd port in IPv6'
    if msg:
        utilities.reporter(msg, 'red')
        return False
    return True


def driver_restart(host_obj):
    msg = ''
    if hostSetData.driver_action(host_obj, 'restart') is None:
        msg += ' fail to restart the driver in host: ' + host_obj.get_hostname()
    if msg:
        utilities.reporter(msg, 'red')
        return False
    return True
