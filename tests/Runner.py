#!/usr/bin/python
"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-5136306
This file is saving the mainly globals parameters in my project
"""
import easygui as eg
import tests
import globals


class Runner(object):
    _Runner_Instance = None
    tests = []
    results = []

    def __init__(self):
        if Runner._Runner_Instance != None:
            raise Exception('Singleton Class - cant create another object!')
        question = "Choose Test - Cases:"
        title = "Mini - Runner"
        listOfOptions = ["IPv4 ping", "IPv6 ping",
                         "Server_Driver_Restart", "Client_Driver_Restart",
                         "Update Server - Not Implement Yet", "Update Client - Not Implement Yet"]
        choice = eg.multchoicebox(question, title, listOfOptions)

        for test in choice:
            self.tests.append(test)

    def run_me(self):
        for test in self.tests:
            if test == 'IPv4 ping':
                if self.ping_test_ipv4:
                    self.results.append("IPv4 ping test pass!\n")
                else:
                    self.results.append("IPv4 ping test fail!\n")
            elif test == 'IPv6 ping':
                if self.ping_test_ipv6():
                    self.results.append("IPv6 ping test pass!\n")
                else:
                    self.results.append("IPv6 ping test fail!\n")
            elif test == 'Server_Driver_Restart':
                if self.driver_restart_server():
                    self.results.append("Server - Driver Restart test pass!\n")
                else:
                    self.results.append("Server - Driver Restart test fail!\n")
            elif test == 'Client_Driver_Restart':
                if self.driver_restart_client():
                    self.results.append("Client - Driver Restart test pass!\n")
                else:
                    self.results.append("Client - Driver Restart test fail!\n")

    # @property - ?????
    def ping_test_ipv4(self):
        return tests.ping_test_ipv4()

    def ping_test_ipv6(self):
        return tests.ping_test_ipv6()

    def driver_restart_client(self):
        return tests.driver_restart(globals.hostLinuxClient)

    def driver_restart_server(self):
        return tests.driver_restart(globals.hostLinuxServer)

    def display_results(self):
        msg = "Report Details:"
        title = "Mini - Runner"
        eg.textbox(msg, title, self.results)
