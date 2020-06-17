
import unittest
import time
import subprocess
from queue import Queue
import re

from utils import driver
from utils import read_messaging_logs
from utils import xml_parsing
from utils import string_list as sl
from components import components_operations

class WebFiltering (unittest.TestCase):

    def test_web_filtering(self):
        device = driver.child_device
        print("device:",device)
        global logs
        # get keepers logcats to a PIPE
        process = subprocess.Popen(['adb', '-s', device, 'logcat', '-s', 'HttpKeepersLogger'],
                                   stdout=subprocess.PIPE)
        stdout_queue = Queue()
        stdout_reader = read_messaging_logs.AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.start()

        applications = xml_parsing.tests_xml_to_dictionary(sl.NETWORKS_FILE)
        print(applications)
        for application in applications:
            if application[sl.S_NETWORK_NAME] == driver.current_test[sl.TEST_APP_NAME]:
                driver.connect_driver(application[sl.APP_PACKAGE], application[sl.APP_ACTIVITY])  # connect the driver
                for step in application[sl.STEPS]:
                    print("hii")
                    driver.global_tests_result.append(components_operations.component_operation(step))
                    time.sleep(1)
                subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'keyevent', '66'])

        while not stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = stdout_queue.get()
            #TODO check the log structure
            if "taggedText" in str(line):
                logs.append(str(line))