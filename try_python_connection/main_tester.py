'''
This file handles the running of the tests
there is 2 attributes:
tests_results: list of all the tests results
flowes: list of all the flowes
'''

import unittest
import subprocess
import os
# from appium.webdriver.appium_service import AppiumService
from utils import driver
from utils import xml_parsing
from utils import string_list as sl
import time
from features import messaging
from features import web_filtering
from features import device_locked


tests_results = []
flowes = []
messaging_functions = {'whatsapp':'whatsapp_message'}

class MainTester(unittest.TestCase):




    def run_messaging_feature_test(self, test_name, s_network_name):
        # os.system("start cmd.exe @cmd /k appium ")
        print("My love ---1\n")
        # time.sleep(5)
        # tests = xml_parsing.feature_xml_to_dictionary(sl.MESSAGING_FEATURE_FILE)# converts the xml file to list of diction
        # for test in tests:
        #     if test[sl.TEST_NAME] == test_name or test_name == sl.ALL:
        #         test[sl.TEST_APP_NAME] = s_network_name
        #         driver.current_test = test
        #         if test_name == "Signing in is not allowed":
        #             suite = unittest.TestLoader().loadTestsFromTestCase(web_filtering.WebFiltering)
        #             result = unittest.TextTestRunner(verbosity=1).run(suite)
        #             return
        #         elif test_name == "device lock":
        #             suite = unittest.TestLoader().loadTestsFromTestCase(device_locked.DeviceLocked)
        #             result = unittest.TextTestRunner(verbosity=1).run(suite)
        #             print("the test result: ",result)
        #             return
        #         suite = unittest.TestLoader().loadTestsFromTestCase(messaging.Messaging)
        #         result = unittest.TextTestRunner(verbosity=1).run(suite)
        #         tests_results.append("test: {} result: {}".format(test[sl.TEST_NAME], result))  # save the test result





    def run_web_filtering_test(self, test_name):
        print("My love ---2\n")
        # tests = xml_parsing.feature_xml_to_dictionary(
        #     sl.MESSAGING_FEATURE_FILE)  # converts the xml file to list of diction
        # for test in tests:
        #     if test[sl.TEST_NAME] == test_name or test_name == sl.ALL:
        #         suite = unittest.TestLoader().loadTestsFromTestCase(web_filtering.WebFiltering)
        #         result = unittest.TextTestRunner(verbosity=1).run(suite)
        #         tests_results.append("test: {} result: {}".format(test[sl.TEST_NAME], result))  # save the test result