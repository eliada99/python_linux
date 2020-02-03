"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-525136306
"""
import datetime

from modules import utilities
import globals

REPORT_PATH = "objects/web2/results/"


class WebBrowserRunner(object):
    _Web_Instance = None

    def __init__(self):
        if WebBrowserRunner._Web_Instance is not None:
            raise Exception('Singleton Class - cant create another object!')

        self.start_date = utilities.get_current_time()
        file_name = REPORT_PATH + "automation_results_" + str(self.start_date) + ".html"
        self.file_name = file_name
        f = open(file_name, 'w')

        message = """<html>
        <head>
        <title>Mini - Runner</title>
        </head>
        <body>
        
        <h1>Automation Running Results:</h1>
        <p>W - I - P...</p>
        <p>Automation is running now..</p>
        
        </body>
        </html>"""

        f.write(message)
        f.close()

    def add_content(self, res_list):
        now = datetime.datetime.now()
        now = now.strftime("%c")
        content = "Report Details:<br>Start Date: " + globals.runner.start_date + "<br>End Date:    " + now + "<br>" + \
                   globals.hostLinuxServer.print_me() + "<br>" + globals.hostLinuxClient.print_me()

        f = open(self.file_name, 'w')
        message = """<html>
        <head></head>
        <body><p>"""
        message += content
        message += "<br>Results:<br>"
        for res in res_list:
            message += res + "<br>"
        message += """</p></body>
        </html>"""

        f.write(message)
        f.close()

    def get_file_name(self):
        return self.file_name
