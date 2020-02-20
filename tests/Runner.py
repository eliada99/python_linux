#!/usr/bin/python
"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-5136306
This file is saving the mainly globals parameters in my project
"""
import datetime
import easygui as eg
import tests
import globals


class Runner(object):
    _Runner_Instance = None
    tests = []
    results = []
    start_date = datetime.datetime.now()
    start_date = start_date.strftime("%c")

    def __init__(self):
        if Runner._Runner_Instance is not None:
            raise Exception('Singleton Class - cant create another object!')
        question = "Choose Test - Cases:"
        title = "Mini - Runner"
        list_of_options = ["Update_Server", "Update_Client",
                           "Server_Driver_Restart", "Client_Driver_Restart",
                           "IPv4 ping", "IPv6 ping"]
        choice = eg.multchoicebox(question, title, list_of_options)

        for test in choice:
            self.tests.append(test)

    def run_me(self):
        """In function: Runner.run_me - choose tests and start running [via basic GUI]"""
        for test in self.tests:
            if test == 'IPv4 ping':
                if self.ping_test_ipv4():
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
            elif test == 'Update_Server':
                if self.update_setup_server():
                    self.results.append("Server - Update Driver: test pass!\n")
                else:
                    self.results.append("Server - Update Driver: test fail!\n")
            elif test == 'Update_Client':
                if self.update_setup_client():
                    self.results.append("Client - Update Driver: test pass!\n")
                else:
                    self.results.append("Client - Update Driver: test fail!\n")

    def ping_test_ipv4(self):
        return tests.ping_test_ipv4()

    def ping_test_ipv6(self):
        return tests.ping_test_ipv6()

    def driver_restart_client(self):
        return tests.driver_restart(globals.hostLinuxClient)

    def driver_restart_server(self):
        return tests.driver_restart(globals.hostLinuxServer)

    def update_setup_server(self):
        return tests.update_setup(globals.hostLinuxServer)

    def update_setup_client(self):
        return tests.update_setup(globals.hostLinuxClient)

    def get_results(self):
        return self.results

    def display_results(self, res_file):
        """in function: Runner.display_results - Show basic GUI with the results"""
        now = datetime.datetime.now()
        now = now.strftime("%c")
        msg = "For full results and setup details: " + res_file
        title = "Mini - Runner"
        eg.textbox(msg, title, self.results)
