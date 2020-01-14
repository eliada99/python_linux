#!/usr/bin/python
"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-525136306
"""
from os import sys, path
import datetime
# My project import
import globals
from objects.web2.WebBrowserRunner import WebBrowserRunner

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


# ---------- Main code ----------
if __name__ == '__main__':
    web = WebBrowserRunner()
    globals.init()
    globals.runner.run_me()

    now = datetime.datetime.now()
    now = now.strftime("%c")
    msg = "Report Details:<br>Start Date: " + globals.runner.start_date + "<br>End Date:    " + now + "<br>" + \
          globals.hostLinuxServer.print_me() + "<br>" + globals.hostLinuxClient.print_me()

    web.add_content(msg, globals.runner.get_results())

    globals.runner.display_results()
