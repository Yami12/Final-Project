"""
this file interacts with the GUI and runs all the tests
"""

import sys
import unittest
import os

from utils import driver
from utils import xml_parsing
from utils import string_list as sl
from utils import html_page
from utils import utils_funcs as uf

from features import messaging
from features import web_filtering
from features import device_locked

from components import components_tests




if __name__ == '__main__':
    result = " "
    try:
        test_name = ""

        uf.print_log("{\\rtf1\\ansi\deff0{\colortbl;\\red0\green0\\blue0;\\red255\green0\\blue0;\\red0\green255\\blue0;}}")#defines the logs colors

        if sys.argv[1] == sl.FEATURE_TEST: # feature test
            test_name = sys.argv[2] # test name
            app_name = sys.argv[3]  # app name
            driver.father_device = sys.argv[4] # parent device
            driver.child_device = sys.argv[5] # child device
            driver.tests_folders_names = sys.argv[6]

            uf.print_log("\cf1 initializing parent driver.\line")
            driver.initialize(driver.father_device)

            tests = xml_parsing.feature_xml_to_dictionary(
                sl.MESSAGING_FEATURE_FILE)  # gets the list of all the tests

            for test in tests:
                if test[sl.TEST_NAME] == test_name:
                    uf.print_log("\cf1 start to run test: " + str(test_name) + "\line")

                    test[sl.TEST_APP_NAME] = app_name
                    driver.current_test = test
                    driver.global_tests_result.append({sl.TEST_RESULTS_NAME: test_name, sl.TEST_RESULTS: []}) # saves the current test results

                    if test_name == sl.WEB_TEST: # Web filtering test
                        # run the test
                        suite = unittest.TestLoader().loadTestsFromTestCase(web_filtering.WebFiltering)
                        unittest.TextTestRunner(verbosity=1).run(suite)
                    elif test_name == sl.DEVICE_LOCK_TEST: # Device locked test
                        # run the test
                        suite = unittest.TestLoader().loadTestsFromTestCase(device_locked.DeviceLocked)
                        unittest.TextTestRunner(verbosity=1).run(suite)
                    else: # Messeging and Removal from group tests
                        # run the test
                        suite = unittest.TestLoader().loadTestsFromTestCase(messaging.Messaging)
                        unittest.TextTestRunner(verbosity=1).run(suite)


        elif sys.argv[1] == sl.COMPONENT_TEST: # component test
            test_name = sys.argv[2]  # test name
            driver.tester_device = sys.argv[3] # tester device
            driver.tests_folders_names = sys.argv[4]

            uf.print_log("\cf1 initializing tester driver.\line")
            driver.initialize(driver.tester_device)

            tests = xml_parsing.tests_xml_to_dictionary(
                sl.COMPONENTS_FILE)  # gets the list of all the tests
            for test in tests:
                if test[sl.TEST_NAME] == test_name or test_name == sl.ALL:
                    uf.print_log("\cf1 start to run test: " + test_name + "\line")
                    driver.current_test = test
                    driver.global_tests_result.append({sl.TEST_RESULTS_NAME: test_name, sl.TEST_RESULTS: []})# saves the current test results
                    #run the test
                    suite = unittest.TestLoader().loadTestsFromTestCase(components_tests.ComponentsTest)
                    result = unittest.TextTestRunner(verbosity=1).run(suite)


        elif sys.argv[1] == sl.MAIL: # send the test's result to mail
            html_page.send_email(sys.argv[2])
            os._exit(0)

        uf.print_log("\cf1 \\b creating HTML file with the test results \\b0 \line")
        html_page.create_html_file(test_name)

        if driver.test_result == True:
            uf.print_log("\cf3 \\b TEST PASSED \\b0 \line")
            os._exit(0)

        elif driver.test_result == False:
            uf.print_log("\cf2 \\b TEST FAILED \\b0 \line")
            os._exit(1)
        else:
            uf.print_log("\cf2 \\b TEST ERROR \\b0 \line")
            os._exit(-1)

    except:
        uf.print_log("\cf3 \\b TEST ERROR \\b0 \line")
        os._exit(-1)

