import os
import re
import time

import paramiko
from paramiko import Channel
from clires import CliResults

#from src.mlnx.qa.core.infra.reporter.logger.logger import Log
from listener import SshListener
from timeout import ReadTimeOut
from filelistener import FileReadListener
#from src.mlnx.qa.core.infra.reporter.report.report import Reporter



class SshConn:
    '''
    create ssh connection session\n
    add listener to each session
    Erez.s
    '''


    def __init__(self, host, username, password, prompt):
        '''
        initialized ssh connection
        raise an `.SSHException` if connection
        '''
        self.clires = None
        self.host = host
        self.username = username
        self.password = password
        self.prompt = prompt
        self.listener = None
        self.readTimeOut = None
        self.cmdTimeOut = False
        self.maxtime = 10
        self.silence = False
        self.conn_timeoute = 10

        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #Reporter._reporter.addStep("connect ssh to :"+ host,"","pass")
        print("connect ssh to :" + host, "", "pass")

        self.client.connect(hostname=self.host,username=self.username, password=self.password,
                            timeout=self.conn_timeoute)

        self.rc = self.client.invoke_shell(term='vt100')

        #Reporter._reporter.dbResultsEntry.set_expected_message("ssh connected")
        print("ssh connected")

    def open(self, tofile=False):
        print("ssh open listener session")

        if tofile:
            self.listener = FileReadListener(self.rc, self.prompt)
        else:
            self.listener = SshListener(self.rc, self.prompt)

        self.readTimeOut = ReadTimeOut(self)
        self.listener.readTimeOut = self.readTimeOut

        self.listener.start()

        self.readTimeOut.setMaxTime(self.maxtime)
        self.readTimeOut.start()

        while not self.listener.prompt_appear and not self.cmdTimeOut:
            time.sleep(0.5)

        # stop read timeout
        if not self.cmdTimeOut:
            self.readTimeOut.cont = False
            self.readTimeOut.join()

        if self.cmdTimeOut:
            self.stop_prc()

        return self

    # was: def send(self, data, prompt=None, ret='\n', timeout=30, silence=False)->CliResults:
    def send(self, data, prompt=None, ret='\n', timeout=30, silence=False):

        if prompt is not None:
            self.prompt = prompt

        self.clires = CliResults()
        self.silence = silence
        self.listener.line = ""
        self.listener.prompt_appear = False
        self.listener.sb = ""

        self.listener.silence = silence
        self.readTimeOut.silence = silence

        if prompt is not None:
            self.prompt = prompt

        if self.cmdTimeOut :
           return


        if prompt is not None:
            self.listener.prompt = prompt


        if timeout is not None:
            self.maxtime = timeout
            self.readTimeOut.setMaxTime(self.maxtime)
            self.readTimeOut.start()

        if not self.silence:
            #Log.logger.rawPrint(data)
            print(data)
            #Reporter._reporter.addStep("ssh command : " + data, "", "pass")
            print("ssh command : " + data, "", "pass")

        self.rc.send(data + ret)


        while not self.listener.prompt_appear and not self.cmdTimeOut:
            time.sleep(0.1)


        if  self.cmdTimeOut :
            self.stop_prc()


        # stop read timeout
        if timeout is not None and not self.cmdTimeOut:
            self.readTimeOut.cont = False
            self.readTimeOut.join()

        out = self.listener.sb

        # remove prompt
        if self.prompt in out:
            lastLisne = re.search('^.*'+self.prompt, out, flags=re.MULTILINE).group(0)
            out = out[0:out.rfind(lastLisne)]

        self.listener.sb = ""
        self.listener.line = ""

        self.clires.out = out
        self.clires.command = data
        if self.rc.exit_status_ready():
             self.clires.exit_status = self.rc.recv_exit_status()

        return self.clires



    def sendDontWait(self, data):
        self.listener.buff = False
        #Reporter._reporter.addStep("ssh command : " + data, "", "pass")
        print("ssh command : " + data, "", "pass")
        self.rc.send(data + '\n')
        return self


    def stop_prc(self):
        self.readTimeOut.cont = False
        self.readTimeOut.join()
        self.close()
        out = self.listener.sb
        self.listener.sb = ""
        self.listener.line = ""
        raise Exception('ssh read command timeout [ more then = '+ str( self.maxtime) +" sec ]")


    def close(self):
        try:
            if not self.silence:
                #Reporter._reporter.addStep("close ssh session to : " + str(self.host))
                print("close ssh session to : " + str(self.host))
            self.listener.stopListener()
            self.listener.join()
            self.readTimeOut.join()
            self.client.close()
        except Exception:
            pass