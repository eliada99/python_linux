import time
from threading import Thread


class ReadTimeOut(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.max_time_sec  = None
        self.cont = True
        self.name = "ssh_timeout"
        self.sshConn = conn
        self.daemon = True
        self.silence = True

    def run(self):
        counter = 0
        self.cont=True
        while self.cont and counter < self.max_time_sec:
            time.sleep(1)
            counter +=1
            # if not self.silence:
            #     print("timeout :" + str(counter) +":" +str(self.max_time_sec))

        if self.cont :
            try:
                self.sshConn.cmdTimeOut = True
            except Exception:
                pass



    def setMaxTime(self, timeOut):
        Thread.__init__(self,name="ssh_timeout")
        self.max_time_sec = timeOut
