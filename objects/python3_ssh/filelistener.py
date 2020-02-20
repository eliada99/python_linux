import os
import time

from listener import SshListener
#from src.mlnx.qa.core.infra.reporter.logger.logger import Log
#from src.mlnx.qa.core.infra.reporter.report.report import Reporter
from config import RunConfig


class FileReadListener(SshListener):

    def __init__(self, rc, prompt):
        SshListener.__init__(self,rc, prompt)
        self.name = "fileLisener"

        self.fname = str(round(time.time_ns()))+".html"
        self.path = RunConfig.resultsPath + "/" + self.fname

        #Log.logger.info(self.path)
        print(self.path)

        self.file = open(self.path, "a")
        self.fileIo = open(self.path, 'r')
        self.filePointer=-1

        self.linkPath()

    def run(self):
        while self.runThread:
            while not self.rc.recv_ready() and self.runThread:
                time.sleep(0)

            if not self.runThread:
                break

            out = self.rc.recv(32768).decode('utf-8')
            self.file.write("<p>" +out+"</p")
            self.file.flush()

            outlast = self.fileIo.read()

            if self.prompt in outlast:
                self.readTimeOut.cont = False
                self.prompt_appear = True


    def linkPath(self):
        backend = str(RunConfig.frameworkConf.getOption("Gui","backend"))
        screen_capture =str( RunConfig.frameworkConf.getOption("Files","screen_capture"))

        p = screen_capture + RunConfig.resultsFolder + "/"+ self.fname
        link = "<a href=/file-read?file=/"+ p + "&is_web=true target='_blank' >link</a>"
        #Reporter._reporter.addStep("link to file :" ,link , "pass")
        print("link to file :" ,link , "pass")

