
import unittest
import time
import subprocess
from queue import Queue


from utils import driver
from utils import read_messaging_logs
from utils import xml_parsing
from utils import string_list as sl

from features import messaging

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

        applications = xml_parsing.tests_xml_to_dictionary(sl.APPS_FILE)
        for application in applications:
            if application[sl.APP_NAME] == driver.current_test[sl.TEST_APP_NAME]: #open the app
                subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'start', '-n',
                                application[sl.APP_PACKAGE] + "/" + application[sl.APP_ACTIVITY]])
                for step in application[sl.STEPS]:
                    if step[sl.ACTION_STEP] == sl.ACTION_SEND_KEYS:
                        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text',
                                        driver.current_test[sl.WEBSITE_ADDRESS]])
                    elif step[sl.ACTION_STEP] == sl.ACTION_CLICK:
                        coordinates = messaging.Messaging.return_coordinates_by_resource_id(messaging.Messaging, step, "")
                        subprocess.run(
                            ['adb', '-s', driver.child_device, 'shell', 'input', 'tap', coordinates[1], coordinates[2]])

                    time.sleep(1)
                subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'keyevent', '66'])

        while not stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = stdout_queue.get()
            print("line= ", line)
            #TODO check the log structure
            if "taggedText" in str(line):
                logs.append(str(line))
