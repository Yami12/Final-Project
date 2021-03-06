import sys
import unittest
import os
import time

from utils import driver
from utils import xml_parsing
from utils import string_list as sl

from features import messaging
from features import web_filtering
from features import device_locked

from components import components_tests




if __name__ == '__main__':

    try:
        os.system("start cmd.exe @cmd /k appium ")
        time.sleep(5)

        if sys.argv[1] == sl.FEATURE_TEST: # feature test
            test_name = sys.argv[2] # test name
            app_name = sys.argv[3]  # app name
            driver.father_device = sys.argv[4] # parent device
            driver.child_device = sys.argv[5] # child device

            driver.initialize(driver.father_device)

            tests = xml_parsing.feature_xml_to_dictionary(
                sl.MESSAGING_FEATURE_FILE)  # converts the xml file to list of dictionaries
            for test in tests:
                if test[sl.TEST_NAME] == test_name or test_name == sl.ALL:
                    test[sl.TEST_APP_NAME] = app_name
                    driver.current_test = test
                    driver.global_tests_result.append({"name": test_name, "results": []})
                    if test_name == sl.WEB_TEST:
                        suite = unittest.TestLoader().loadTestsFromTestCase(web_filtering.WebFiltering)
                        result = unittest.TextTestRunner(verbosity=1).run(suite)
                    elif test_name == sl.DEVICE_LOCK_TEST:
                        suite = unittest.TestLoader().loadTestsFromTestCase(device_locked.DeviceLocked)
                        result = unittest.TextTestRunner(verbosity=1).run(suite)
                    else:
                        suite = unittest.TestLoader().loadTestsFromTestCase(messaging.Messaging)
                        result = unittest.TextTestRunner(verbosity=1).run(suite)

        elif sys.argv[1] == sl.COMPONENT_TEST: # component test
            test_name = sys.argv[2]  # test name
            driver.tester_device = sys.argv[3] # tester device

            driver.initialize(driver.tester_device)

            tests = xml_parsing.tests_xml_to_dictionary(
                sl.COMPONENTS_FILE)  # converts the xml file to list of dictionaries
            for test in tests:
                if test[sl.TEST_NAME] == test_name or test_name == sl.ALL:
                    driver.current_test = test
                    suite = unittest.TestLoader().loadTestsFromTestCase(components_tests.ComponentsTest)
                    result = unittest.TextTestRunner(verbosity=1).run(suite)
                    driver.global_tests_result.append({"name": test_name, "results": []})

    except:
        print("One or more parametrs are missing\nPlease try again.")
        exit(1)
    exit(0)
