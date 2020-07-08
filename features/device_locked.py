"""
This file handles the child device locked test
"""
import unittest
import time
import subprocess
from queue import Queue
import datetime
import json

from utils import driver
from utils import read_messaging_logs
from utils import xml_parsing
from utils import string_list as sl
from utils import utils_funcs as uf

from components import components_operations


logs = []

class DeviceLocked (unittest.TestCase):

    '''
        check if the expected log exist in the received logs
        and save the result (if exist or not)
    '''
    def check_keepers_logs(self):
        global logs
        for i in range(0, len(logs)):
            if "start" in logs[i]:
                if uf.time_in_range(int(logs[i].split('"start": ')[1].split(",\\r\\n")[0]), 1) == True and (
                    uf.time_in_range(int(logs[i+1].split('"end": ')[1].split("\\r\\n")[0]), 4) == True) and (
                    logs[i+2].split('"didStart":')[1].split("}\\r\\n")[0] == "true"):
                    driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_PASSED, "The found log is : " + json.dumps(logs[i])])
                    driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_PASSED, "The child device is locked"])
                    uf.print_log("\cf1 The found log is : " + json.dumps(logs[i]) + "\line \cf3 The child device is locked \line")
                    return True
        uf.print_log("\cf2 No matching logs \line The child device is not locked \line")
        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "No matching logs"])
        driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_FAILED, "The child device is not locked"])
        return False

    '''
        A function that performs the child device locked test 
        and sends the function to check whether the device is actually locked
    '''
    def test_device_locked(self):
        global logs
        uf.print_log("\cf1 locking child device. \line begin to listen to child logs \line")
        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "locking child device"])
        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "begin to listen to child logs"])
        # get keepers logcats in child device
        process = subprocess.Popen(['adb', '-s', driver.child_device, 'logcat', '-s', 'HttpKeepersLogger'],
                                   stdout=subprocess.PIPE)
        stdout_queue = Queue()
        stdout_reader = read_messaging_logs.AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.start()

        applications = xml_parsing.tests_xml_to_dictionary(sl.APPS_FILE) # get the list of all the apps
        for application in applications:
            if application[sl.APP_NAME] == sl.KEEPERS_DEVICE_LOCKED:   # Keepers app
                uf.print_log("\cf1 connecting to appium server \line")
                driver.connect_driver(application[sl.APP_PACKAGE], application[sl.APP_ACTIVITY])  # connect the driver
                time.sleep(6)

                uf.print_log("\cf1 starting to run the test steps \line")
                driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "starting to run the test steps"])
                #  run all the steps on the parent device to lock the child device
                for step in application[sl.STEPS]:
                    if step[sl.TYPE_STEP] == sl.TYPE_CLASS: #this is the step that define the end time
                        component = driver.global_driver.find_elements_by_class_name(step[sl.ID_STEP])
                        text = int(component[7].get_attribute("text"))
                        if text > 57:   #need to move to the next hour
                            text2 = component[6].get_attribute("text")
                            component[6].click()
                            component[6].clear()
                            component[6].send_keys(str(int(text2) + 1))
                            driver.global_driver.press_keycode(66)
                        component[7].click()
                        component[7].clear()
                        component[7].send_keys(str((text + 3) % 60))    #the end time is 3 minute from the current time
                        driver.global_driver.press_keycode(66)
                        continue
                    driver.global_tests_result[-1][sl.TEST_RESULTS].append(components_operations.component_operation(step))
                    time.sleep(2)
                driver.sending_time = datetime.datetime.now() # save the locking time
        time.sleep(10)

        uf.print_log("\cf1 checking if the child's device is locked \line")
        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "checking if the child's device is locked"])
        upload_process = subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'broadcast', '-a',
                        'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS']) # upload keepers locked
        time.sleep(15)

        flag_timeRange = 0
        while not stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = str(stdout_queue.get())
            if flag_timeRange > 0:  #enter the 2 fileds in timeRange (start and end)
                logs.append(line)
                flag_timeRange = flag_timeRange - 1
            elif "timeRange" in line: #need to save the next 2 lines
                flag_timeRange = 2
            elif "didStart" in line:
                logs.append(line)

        uf.print_log("\cf1 checking child logs \line")
        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "checking child logs"])
        driver.test_result = self.check_keepers_logs()
        process.kill()
        upload_process.kill()
