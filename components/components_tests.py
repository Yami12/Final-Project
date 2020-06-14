'''
This file handles the button resource operations
'''

from selenium.webdriver import ActionChains
from utils import driver
import unittest
import re
from utils import xml_parsing
import time
from components import components_operations
from utils import string_list as sl

class ComponentsTest(unittest.TestCase):
    '''
        function:check_expected_result
        description: checks if the result of the operation is the same as the test's expected result
    '''
    def check_expected_result(self, expected_result):
        result = ["Passed", ""]
        if not expected_result == '':
            if re.search("toastMessage:.*", driver.current_test['expectedResult']):# taost message
                result = components_operations.xpath_operation('//android.widget.Toast[1]', sl.ACTION_GET, "")

            elif re.search("labelMessage:.*", driver.current_test['expectedResult']):# label message
                result = components_operations.id_operation('com.keepers:id/textinput_error',sl.ACTION_GET, "")
            print("result: ", result)
            print(expected_result.split(":")[1])
            if (result[0] == 'Passed') and (result[1] == expected_result.split(":")[1]):
                    return result
            result[0] = "Failed"
            result[1] = "Data Mismatch"
        return result



    def test_flow_run(self):

        test = driver.current_test
        driver.connect_driver('com.keepers', 'com.keeper.common.splash.SplashActivity')
        time.sleep(4)
        for step in test[sl.STEPS]:
            result = components_operations.component_operation(step)
            driver.global_tests_result.append("test: {} status: {} description: {}".format(test['name'], result[0], result[1]))
            time.sleep(2)
        print(self.check_expected_result(test[sl.TEST_EXPECTED_RES]))

