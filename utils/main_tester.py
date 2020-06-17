'''
This file handles the running of the tests
there is 2 attributes:
tests_results: list of all the tests results
flowes: list of all the flowes
'''

import unittest
import subprocess
import os
from appium.webdriver.appium_service import AppiumService
from utils import driver
from utils import xml_parsing
from utils import string_list as sl
import time
from features import messaging
from features import web_filtering
from components import components_operations


tests_results = []
flowes = []
messaging_functions = {'whatsapp':'whatsapp_message'}

class MainTester(unittest.TestCase):




    def run_messaging_feature_test(self, test_name, s_network_name):
        # os.system("start cmd.exe @cmd /k appium ")

        time.sleep(5)
        tests = xml_parsing.feature_xml_to_dictionary(sl.MESSAGING_FEATURE_FILE)# converts the xml file to list of diction
        for test in tests:
            if test[sl.TEST_NAME] == test_name or test_name == sl.ALL:
                test[sl.TEST_APP_NAME] = s_network_name
                driver.current_test = test
                if test_name == "Signing in is not allowed":
                    self.run_web_filtering_test(test_name)
                    return
                elif test_name == "device lock":
                    self.run_device_lock_test()
                    return
                suite = unittest.TestLoader().loadTestsFromTestCase(messaging.Messaging)
                result = unittest.TextTestRunner(verbosity=1).run(suite)
                tests_results.append("test: {} result: {}".format(test[sl.TEST_NAME], result))  # save the test result

    def run_device_lock_test(self):
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
                        component[7].send_keys(int(text)+10)
                        continue
                    driver.global_tests_result.append(components_operations.component_operation(step))
                    time.sleep(2)

    def run_web_filtering_test(self, test_name):
        tests = xml_parsing.feature_xml_to_dictionary(
            sl.MESSAGING_FEATURE_FILE)  # converts the xml file to list of diction
        for test in tests:
            if test[sl.TEST_NAME] == test_name or test_name == sl.ALL:
                suite = unittest.TestLoader().loadTestsFromTestCase(web_filtering.WebFiltering)
                result = unittest.TextTestRunner(verbosity=1).run(suite)
                tests_results.append("test: {} result: {}".format(test[sl.TEST_NAME], result))  # save the test result