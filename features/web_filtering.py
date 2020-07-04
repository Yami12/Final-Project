import unittest
import time
import subprocess
from utils import driver
from utils import xml_parsing
from utils import string_list as sl
from features import messaging


class WebFiltering (unittest.TestCase):

    '''
        check if the website is blocked
    '''
    def check_lock_page(self):
        print("check if the website is blocked")
        time.sleep(3)
        process = subprocess.Popen(['adb', '-s', driver.child_device, 'exec-out', 'uiautomator', 'dump', '/dev/tty'],
                                   stdout=subprocess.PIPE)  # dump the uiautomator file
        content = str(process.stdout.read())
        if "Website Is Blocked" in content:
            # the text that appears when the website is locked
            print("passed, the website is blocked")
            driver.global_tests_result[-1]['results'].append(['Passed', 'website is blocked'])
        else:
            print("failed, the website is not blocked")
            driver.global_tests_result[-1]['results'].append(['Failed', 'website is not blocked'])

    '''
        open the website and call function to check if the website is blocked
    '''
    def test_web_filtering(self):
        applications = xml_parsing.tests_xml_to_dictionary(sl.APPS_FILE)
        for application in applications:
            if application[sl.APP_NAME] == driver.current_test[sl.TEST_APP_NAME]: #open the app
                subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'start', '-n',
                                application[sl.APP_PACKAGE] + "/" + application[sl.APP_ACTIVITY]])
                print("try to open the wanted website")
                for step in application[sl.STEPS]:  #do all the steps to open the website
                    if step[sl.ACTION_STEP] == sl.ACTION_SEND_KEYS:
                        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text',
                                        driver.current_test[sl.WEBSITE_ADDRESS]])
                    elif step[sl.ACTION_STEP] == sl.ACTION_CLICK:
                        coordinates = messaging.Messaging.get_coordinates_by_resource_id(messaging.Messaging, step, "")
                        subprocess.run(
                            ['adb', '-s', driver.child_device, 'shell', 'input', 'tap', coordinates[1], coordinates[2]])
                    time.sleep(1)
                subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'keyevent', '66'])
        self.check_lock_page()


