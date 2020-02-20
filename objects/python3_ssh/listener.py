from threading import Thread
import time
from paramiko import Channel
#from src.mlnx.qa.core.infra.reporter.logger.logger import Log
from timeout import ReadTimeOut


class SshListener(Thread):

    def __init__(self, rc, prompt):
        Thread.__init__(self)
        self.rc = rc
        self.prompt = prompt
        self.sb = ""
        self.line = ""
        self.prompt_appear = False
        self.runThread = True
        self.name = "ssh_listener_ip "
        self.read_timeout = False
        self.readTimeOut = None

        self.silence = False


    def run(self):

        while self.runThread:
            # if self.trdTimeOut is not None:
            #     print(self.trdTimeOut.is_alive())
            while not self.rc.recv_ready() and self.runThread :
                time.sleep(0)

            if not self.runThread:
               break

            out = self.rc.recv(32768).decode('utf-8')

            val = str(out).replace("\r", "")

            if not self.silence:
                #Log.logger.rawPrint(val)
                print(val)

            self.sb += out

            if len(self.sb) > 100:
                lastCharBuff = self.sb[-100:]
            else:
                lastCharBuff = self.sb

            print("debug buffer " + lastCharBuff)

            if lastCharBuff.find(self.prompt) >= 0:
                self.readTimeOut.cont = False
                self.prompt_appear = True

    def setPrompt(self, prompt):
        self.prompt = prompt


    def stopListener(self):
        self.runThread = False
        self.rc.close()
        self.filestream = None
        self.prompt_appear = True




