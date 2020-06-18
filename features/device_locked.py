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

class DeviceLocked (unittest.TestCase):

    def test_device_locked(self):
        applications = xml_parsing.tests_xml_to_dictionary(sl.NETWORKS_FILE)
        print(applications)
        for application in applications:
            if application[sl.S_NETWORK_NAME] == "Keepers device lock":
                driver.connect_driver(application[sl.APP_PACKAGE], application[sl.APP_ACTIVITY])  # connect the driver
                time.sleep(6)
                for step in application[sl.STEPS]:
                    print("step: ", step)
                    if step[sl.TYPE_STEP] == sl.TYPE_CLASS:
                        component = driver.global_driver.find_elements_by_class_name(step[sl.ID_STEP])
                        text = component[7].text
                        print("text: ", text)
                        component[7].send_keys(int(text ) +10)
                        continue
                    driver.global_tests_result.append(components_operations.component_operation(step))
                    time.sleep(2)
        time.sleep(20)
        # check if the lock screen is displayed on the child device
        process = subprocess.Popen(['adb', '-s', driver.child_device, 'exec-out', 'uiautomator', 'dump', '/dev/tty'],
                                   stdout=subprocess.PIPE)  # dump the uiautomator file
        content = str(process.stdout.read())
        if "Your phone is currently on downtime. You’ll regain full access once the countdown has ended." in content:
            driver.global_tests_result.append(['PASSED' ,'The child device is locked'])
            return
        driver.global_tests_result.append(['FAILED', 'The child device is not locked'])