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
    web = WebBrowserRunner()  # create the result HTML page with default content

    globals.init()  # collect data from servers and save them in project global objects
    globals.runner.run_me()  # choose tests ti run and start running [via basic GUI]

    web.add_content(globals.runner.get_results())  # cat the results and details into the HTML file
    globals.runner.display_results(web.get_file_name())  # Show basic GUI

    DaddiBreakMe = 1
