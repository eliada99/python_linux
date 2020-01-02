import time
from threading import Thread


class ParallelFunctionResult:
    def __init__(self, method, result):
        self.method = method
        self.result = result

    @property
    def method(self):
        return self.__functionName

    @method.setter
    def method(self, method):
        self.__method = method

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, result):
        self.__result = result


class RunInParallel(Thread):
    pass

    def __init__(self, method, method_param=None, daemon=False, timeout=0):
        Thread.__init__(self)
        self.daemon = daemon
        self.method = method
        self.method_param = method_param
        self.timeout = timeout
        self.methodRes = None

    def run(self):
        time.sleep(self.timeout)
        if self.method_param is not None:
            self.methodRes = ParallelFunctionResult(str(self.method), self.method(*self.method_param))
        else:
            self.methodRes = ParallelFunctionResult(str(self.method), self.method())

    def thread_timeout(self, timeout, exception=False):
        if self.daemon:
            time.sleep(timeout)
            if self.is_alive():
                if exception:
                    raise Exception("the function {self.function.__name__} has reached timeout after {timeout} sec")
                else:
                    self.timeout = True
        else:
            raise Exception("daemon wasn't set")


def start_and_join_list_of_threads(list_of_threads):
    for thread in list_of_threads:
        thread.start()
    for thread in list_of_threads:
        thread.join()


def get_results(list_of_threads):
    results = []
    for thread in list_of_threads:
        try:
            run_result = thread.methodRes.result
            results.append(run_result)
        except:
            raise Exception("Results is missing - " + thread)
    return results
