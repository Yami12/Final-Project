"""
This file handles the web filtering test
blocked requested websites in the child device
"""
import unittest
import time
import subprocess

from utils import driver
from utils import xml_parsing
from utils import string_list as sl
from utils import utils_funcs as uf


class WebFiltering (unittest.TestCase):

    '''
        function: check_lock_page
        description: check if the website is blocked
    '''
    def check_lock_page(self):
        uf.print_log("\cf1 checking if the website is blocked \line")
        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "checking if the website is blocked"])
        time.sleep(3)
        process = subprocess.Popen(['adb', '-s', driver.child_device, 'exec-out', 'uiautomator', 'dump', '/dev/tty'],
                                   stdout=subprocess.PIPE)  # dump the uiautomator file - get the screen components information
        content = str(process.stdout.read())
        process.kill()
        if "Website Is Blocked" in content:
            # the text that appears when the website is blocked
            uf.print_log("\cf3 PASSED, the website is blocked \line")
            driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_PASSED, 'website is blocked'])
            return True
        else:
            uf.print_log("\cf2 FAILED, the website is not blocked \line")
            driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_FAILED, 'website is not blocked'])
            return False



    '''
        function: test_web_filtering
        desc: opens the not allowed website and checks if the website is blocked
    '''
    def test_web_filtering(self):
        applications = xml_parsing.tests_xml_to_dictionary(sl.APPS_FILE) # get the list of all the apps
        for application in applications:
            if application[sl.APP_NAME] == driver.current_test[sl.TEST_APP_NAME]: #open the app
                uf.print_log("\cf1 connecting to child device \line")
                driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "connecting to child device"])
                subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'start', '-n',
                                application[sl.APP_PACKAGE] + "/" + application[sl.APP_ACTIVITY]])
                uf.print_log("\cf1 try to open the requested website \line")
                driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "try to open the requested website"])
                for step in application[sl.STEPS]:  # run all the steps to open the website
                    if step[sl.ACTION_STEP] == sl.ACTION_SEND_KEYS:
                        uf.print_log('\cf1 enter text. run command: adb -s ' + driver.child_device + ' shell input text: "' + str(
                                driver.current_test[sl.WEBSITE_ADDRESS]) + '"\line')
                        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", 'enter text. run command: adb -s ' + driver.child_device + ' shell input text: "' + str(
                                driver.current_test[sl.WEBSITE_ADDRESS])])
                        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text',
                                        driver.current_test[sl.WEBSITE_ADDRESS]])
                    elif step[sl.ACTION_STEP] == sl.ACTION_CLICK:
                        coordinates = uf.get_coordinates_by_resource_id(step, "")
                        uf.print_log('\cf1 click. run command: adb -s' + driver.child_device + 'shell input tap ' + str(
                            coordinates[1]) + ' ' + str(coordinates[2]) + "\line")
                        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", 'click. run command: adb -s' + driver.child_device + 'shell input tap ' + str(
                            coordinates[1]) + ' ' + str(coordinates[2])])
                        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'tap', coordinates[1], coordinates[2]])
                    time.sleep(1)

                uf.print_log("\cf1 click ENTER. run command: adb -s" + driver.child_device + "shell input keyevent 66 \line")
                driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "click ENTER. run command: adb -s" + driver.child_device + "shell input keyevent 66"])
                subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'keyevent', '66']) # click 'enter'

        driver.test_result = self.check_lock_page()


