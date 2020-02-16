#!/usr/bin/python
"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-525136306
"""
from os import sys, path
import datetime
# My project import
import globals
from objects.web2.WebBrowserRunner import WebBrowserRunner
from tests import Runner

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# ---------- Main code ----------
if __name__ == '__main__':
    web = WebBrowserRunner()
    print WebBrowserRunner.__doc__

    globals.init()
    print globals.init.__doc__

    globals.runner.run_me()
    print globals.runner.run_me.__doc__

    web.add_content(globals.runner.get_results())
    print WebBrowserRunner.add_content.__doc__

    globals.runner.display_results(web.get_file_name())
    print globals.runner.display_results.__doc__

    DaddiBreakMe = 1
