'''
This file handles the running of the tests
there is 2 attributes:
tests_results: list of all the tests results
flowes: list of all the flowes
'''

import unittest
import os
from utils import driver
from utils import xml_parsing
from utils import string_list as sl
import time
from features import messaging
from features import web_filtering
from features import device_locked


class MainTester(unittest.TestCase):

    def run_messaging_feature_test(self, test_name, app_name):
        os.system("start cmd.exe @cmd /k appium ")

        time.sleep(5)
        tests = xml_parsing.feature_xml_to_dictionary(sl.MESSAGING_FEATURE_FILE)# converts the xml file to list of diction
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





    # def run_web_filtering_test(self, test_name):
    #     tests = xml_parsing.feature_xml_to_dictionary(
    #         sl.MESSAGING_FEATURE_FILE)  # converts the xml file to list of diction
    #     for test in tests:
    #         if test[sl.TEST_NAME] == test_name or test_name == sl.ALL:
    #             suite = unittest.TestLoader().loadTestsFromTestCase(web_filtering.WebFiltering)
    #             result = unittest.TextTestRunner(verbosity=1).run(suite)
