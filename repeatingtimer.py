#!/usr/bin/env python
"""
A thread that acts as a repeating timer that can be started, stopped, restarted and interval changed.
"""

import threading


class RepeatingTimer(threading.Thread):
    """ A Thread class that repeats function calls like a Timer but allows:
        start_timer(), stop_timer(), restart_timer(), change_interval(), terminate()
    :param seconds (float) the interval time between callbacks
    :param name of the thread for identification
    :param sleep_chunk the divisor of the interval for intermediate steps/threading
    :param callback the function that will be executed each interval
    :param log an optional log passed in from the caller
    :param *args optional argument pointers for the callback function
    """

    def __init__(self, seconds, name=None, sleep_chunk=0.25, callback=None, log=None, *args):
        threading.Thread.__init__(self)
        if name is not None:
            self.name = name
        else:
            self.name = str(callback) + "_timer_thread"
        self.interval = seconds
        if callback is None:
            log.warning("No callback specified for RepeatingTimer " + self.name)
        self.callback = callback
        self.callback_args = args
        self.sleep_chunk = sleep_chunk
        self.terminate_event = threading.Event()
        self.start_event = threading.Event()
        self.reset_event = threading.Event()
        self.count = self.interval / self.sleep_chunk
        self.log = log

    def run(self):
        while not self.terminate_event.is_set():
            while self.count > 0 and self.start_event.is_set() and self.interval > 0:
                if self.reset_event.wait(self.sleep_chunk):
                    self.reset_event.clear()
                    self.count = self.interval / self.sleep_chunk
                self.count -= 1
                if self.count <= 0:
                    self.callback(*self.callback_args)
                    self.count = self.interval / self.sleep_chunk

    def start_timer(self):
        self.start_event.set()
        if self.log is not None:
            self.log.info(self.name + " timer started (" + str(self.interval) + " seconds)")

    def stop_timer(self):
        self.start_event.clear()
        self.count = self.interval / self.sleep_chunk
        if self.log is not None:
            self.log.info(self.name + " timer stopped (" + str(self.interval) + " seconds)")

    def restart_timer(self):
        if self.start_event.is_set():
            self.reset_event.set()
        else:
            self.start_event.set()
        if self.log is not None:
            self.log.info(self.name + " timer restarted (" + str(self.interval) + " seconds)")

    def change_interval(self, seconds):
        if self.log is not None:
            self.log.info(self.name + " timer interval changed (" + str(self.interval) + " seconds)")
        self.interval = seconds
        self.restart_timer()

    def terminate(self):
        self.terminate_event.set()
        if self.log is not None:
            self.log.info(self.name + " timer terminated")
