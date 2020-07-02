'''
This file handles the components tests
'''



import unittest
import re
import time
import sys

from components import components_operations

from utils import driver
from utils import string_list as sl

class ComponentsTest(unittest.TestCase):
    '''
               function:check_expected_result
               description: checks if the result of the operation is the same as the test's expected result
    '''
    def check_expected_result(self, expected_result):
        result = ["Passed", ""]
        if not expected_result == '':
            if re.search("labelMessage:.*", driver.current_test[sl.TEST_EXPECTED_RES]):# label message
                result = components_operations.id_operation('com.keepers:id/textinput_error',sl.ACTION_GET, "")
                if (result[0] == 'Passed') and (result[1] == expected_result.split(":")[1]):
                    return result
            elif re.search("wrongMessage:.*", driver.current_test[sl.TEST_EXPECTED_RES]):# label message
                result = components_operations.id_operation('com.keepers:id/snackbar_text',sl.ACTION_GET, "")
                if (result[0] == 'Passed') and (result[1] == expected_result.split(":")[1]):
                    return result
            elif re.search("disabled:.*", driver.current_test[sl.TEST_EXPECTED_RES]):
                element = driver.global_driver.find_element_by_id(expected_result.split("disabled:id:")[1])
                if element.is_enabled() == False:
                    return ["Passed", "Button disabled"]
            #not expected result
            result[0] = "Failed"
            result[1] = "Data Mismatch"
        return result

    '''
           function:test_run
           description: run the current test
    '''
    def test_run(self):
        test = driver.current_test
        print("connecting to appium server...")
        sys.stdout.flush()
        driver.connect_driver('com.keepers', 'com.keeper.common.splash.SplashActivity')
        time.sleep(4)
        print("starting to run the test steps")
        sys.stdout.flush()
        # run all the steps in the test
        for step in test[sl.STEPS]:
            driver.global_tests_result[-1]['results'].append(components_operations.component_operation(step))
            time.sleep(2)
        print("checking expected results")
        sys.stdout.flush()
        result = self.check_expected_result(test[sl.TEST_EXPECTED_RES])
        driver.global_tests_result[-1]['results'].append(result)
        if result[0] == "Passed":
            driver.test_result = True
        else:
            driver.test_result = False
