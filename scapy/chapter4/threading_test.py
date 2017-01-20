import threading
import time
import os

def process_queue(sleep_time=5):
    print "child {} running..\n".format(threading.current_thread().name)
    time.sleep(5)
    print('thread %s ended.\n' % threading.current_thread().name)

# wait for all download threads to finish
def thread(max_threads=5):
    threads = []
    while threads:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)
        while len(threads) < max_threads:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True) # set daemon so main thread can exit when receives ctrl-c
            thread.start()
            thread.join()
            threads.append(thread)
        # all threads have been processed
        # sleep temporarily so CPU can focus execution on other threads
        #time.sleep(5)

if __name__ == '__main__':
    threads = []
    while threads:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)
    print " {} running..\n".format(threading.current_thread().name)
    while len(threads) < 5:
        # can start some more threads
        thread = threading.Thread(target=process_queue)
        thread.setDaemon(True)  # set daemon so main thread can exit when receives ctrl-c
        thread.start()
        threads.append(thread)
    # all threads have been processed
    # sleep temporarily so CPU can focus execution on other threads
    time.sleep(5)