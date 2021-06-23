import func.color as color
from threading import Thread, Lock

threadLock = Lock()
threads = []

class MyThread(Thread):
    def __init__(self, name, funcs, *args, lock=False):
        Thread.__init__(self)
        self.name = name
        self.funcs = funcs
        self.args = args
        self.lock = lock

    def run(self):
        print(color.yellow("[*]") + " Thread @正在运行: " + self.name)
        if self.lock:
            threadLock.acquire()
            self.funcs(*self.args)
            threadLock.release()
        else:
            self.funcs(*self.args)
