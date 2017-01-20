# -*- coding: utf-8 -*-
# multiprocessing
import os
from multiprocessing import Process

# 子进程要执行的代码
def run_proc(name):
    print 'Run child process %s (%s)...' % (name, os.getpid())

if __name__ == '__main__':
    print "parent Process {} ...".format(os.getpid())
    p = Process(target=run_proc,args=('test',))
    print "Process will start"
    p.start()
    p.join()
    print "Process end."
    '''
    if pid == 0:
        print "Child process {0} and my parent is {1}".format(os.getpid(),os.getppid())
    else:
        print "I {0} just created a child process{1}".format(ls.getpid(), pid)
       ''' 
