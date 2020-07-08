'''
This file handles the components tests
'''

import unittest
import re
import time

from components import components_operations

from utils import driver
from utils import string_list as sl
from utils import utils_funcs as uf

class ComponentsTest(unittest.TestCase):
    '''
            function:check_expected_result
            description: checks if the result of the operation is the same as the test's expected result
                         there is 3 types of results: label message, wrong message and button disabled
    '''
    def check_expected_result(self, expected_result):
        result = [sl.TEST_PASSED, ""]
        if not expected_result == '':
            if re.search("labelMessage:.*", driver.current_test[sl.TEST_EXPECTED_RES]):# label message
                result = components_operations.id_operation('com.keepers:id/textinput_error',sl.ACTION_GET, "")
                if (result[0] == sl.TEST_PASSED) and (result[1] == expected_result.split(":")[1]):
                    uf.print_log("\cf1 " + result[0] + ", " + result[1] + "\line")
                    return result
            elif re.search("wrongMessage:.*", driver.current_test[sl.TEST_EXPECTED_RES]):# wrong message
                result = components_operations.id_operation('com.keepers:id/snackbar_text',sl.ACTION_GET, "")
                if (result[0] == sl.TEST_PASSED) and (result[1] == expected_result.split(":")[1]):
                    uf.print_log("\cf1 " + result[0] + ", " + result[1] + "\line")
                    return result
            elif re.search("disabled:.*", driver.current_test[sl.TEST_EXPECTED_RES]): # button disabled
                element = driver.global_driver.find_element_by_id(expected_result.split("disabled:id:")[1])
                if element.is_enabled() == False:
                    uf.print_log("\cf1 Passed, Button disabled \line")
                    return [sl.TEST_PASSED, "Button disabled"]
            #not expected result
            result[0] = sl.TEST_FAILED
            result[1] = "Expected result Mismatch"
            uf.print_log("\cf2 Failed, Expected result Mismatch \line")
        return result

    '''
           function:test_run
           description: run the current component test
    '''
    def test_run(self):
        test = driver.current_test
        uf.print_log("\cf1 connecting to appium server \line")
        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "connecting to appium server"])
        driver.connect_driver('com.keepers', 'com.keeper.common.splash.SplashActivity')
        time.sleep(4)

        uf.print_log("\cf1 starting to run the test steps \line")
        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "starting to run the test steps"])
        # run all the steps in the test
        for step in test[sl.STEPS]:
            driver.global_tests_result[-1][sl.TEST_RESULTS].append(components_operations.component_operation(step))
            time.sleep(2)

        uf.print_log("\cf1 checking expected results \line")
        driver.global_tests_result[-1][sl.TEST_RESULTS].append(["WIP", "checking expected results"])
        result = self.check_expected_result(test[sl.TEST_EXPECTED_RES])
        driver.global_tests_result[-1][sl.TEST_RESULTS].append(result)
        if result[0] == sl.TEST_PASSED:
            driver.test_result = True
        else:
            driver.test_result = False
