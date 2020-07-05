'''
This file create an asynchronous File reader class
this class is used for reading logs
'''

import threading
from queue import Queue

class AsynchronousFileReader(threading.Thread):

    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''
    def __init__(self, fd, queue):
        assert isinstance(queue, Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self._fd = fd
        self._queue = queue

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def stopped(self):
        '''Check whether there is no more content to expect.'''
        if self._queue.empty():
            self._running = False
            return True
        return False


