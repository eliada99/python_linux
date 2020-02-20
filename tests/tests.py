#!/usr/bin/python

from modules import hostGetData, Parallel
from modules import hostSetData
import globals
from modules import benchmark
from modules import utilities


def ping_test_ipv4():
    threads_list = [Parallel.RunInParallel(benchmark.run_ping,
                    method_param=(globals.hostLinuxClient, globals.serverInterfaceEth1,
                                  globals.clientInterfaceEth1, "ipv4"), timeout=1),
                    Parallel.RunInParallel(benchmark.run_ping,
                    method_param=(globals.hostLinuxClient, globals.serverInterfaceEth2,
                                  globals.clientInterfaceEth2, "ipv4"), timeout=1)]
    Parallel.start_and_join_list_of_threads(threads_list)
    threads_list = Parallel.get_results(threads_list)
    if not threads_list[0] or not threads_list[1]:
        return False
    return True


def ping_test_ipv6():
    threads_list = [Parallel.RunInParallel(benchmark.run_ping,
                    method_param=(globals.hostLinuxClient, globals.serverInterfaceEth1,
                                  globals.clientInterfaceEth1, "ipv6"), timeout=1),
                    Parallel.RunInParallel(benchmark.run_ping,
                    method_param=(globals.hostLinuxClient, globals.serverInterfaceEth2,
                                  globals.clientInterfaceEth2, "ipv6"), timeout=1)]
    Parallel.start_and_join_list_of_threads(threads_list)
    threads_list = Parallel.get_results(threads_list)
    if not threads_list[0] or not threads_list[1]:
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


def update_setup(host_obj):
    msg = ''
    dic_versions = hostGetData.get_versions_from_json()

    try:
        if not hostSetData.install_driver(host_obj, dic_versions["ofed_install_command"]):
            msg = 'fail to update setup: ' + host_obj.get_hostname()
        if hostSetData.driver_action(host_obj, 'restart') is None:
            msg = msg + '\n fail to restart driver'
    except:
        utilities.reporter("OFED installation failed: " + dic_versions["ofed_install_command"] + "\n", 'red')
        return False
    if msg:
        utilities.reporter(msg, 'red')
        return False
    return True
