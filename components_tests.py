'''
This file handles the button resource operations
'''

from selenium.webdriver import ActionChains
import driver
import unittest
import re
import xml_parsing
import components_operations

class ComponentsTest(unittest.TestCase):
    '''
        function:check_expected_result
        description: checks if the result of the operation is the same as the test's expected result
    '''
    def check_expected_result(self):
        result = ["Passed", ""]
        if not driver.current_test['expectedResult'] == '':
            if re.search("toastMessage:.*", driver.current_test['expectedResult']):# taost message
                result = components_operations.toast_operation('//android.widget.Toast[1]')

            if re.search("labelMessage:.*", driver.current_test['expectedResult']):# label message
                result = components_operations.label_operation('com.keepers:id/textinput_error')
            if (result[0] == 'Passed') and (result[1] == driver.current_test['expectedResult'].split(":")[1]):
                    return result
            result[0] = "Failed"
            result[1] = "Data Mismatch"
        return result



    def test_flow_run(self):
        driver.initialize_father('com.keepers', 'com.keeper.common.splash.SplashActivity')

        flowes = xml_parsing.component_xml_to_dictionary(
            "components_behavior_tests.xml")  # converts the xml file to list of dictionaries
        # go over all the flowes
        for flow in flowes:
            if flow['name'] == driver.requested_flow:  # the desired flow
                for test in flow['tests']:
                    driver.current_test = test
                    # button or checkbox
                    if test['type'] == 'Button' or test['type'] == 'CheckBox':
                        result = components_operations.button_operation(driver.current_test['resourceId'],driver.current_test['action'])
                        driver.global_tests_result.append("test: {} status: {} description: {}".format(flow['name'],
                                                                                   result[0], result[1]))

                        components_operations.check_expected_result()
                    elif test['type'] == 'Entry':
                        result = components_operations.input_operation(driver.current_test['resourceId'],driver.current_test['content'])
                        driver.global_tests_result.append("flow: {} test: {} status: {} description: {}".format(flow['name'], test['name'],
                                                                                  result[0], result[1]))
                    result = ComponentsTest.check_expected_result()
                    driver.global_tests_result.append(
                        "flow: {} test: {} status: {} description: {}".format(flow['name'], test['name'],
                                                                              result[0], result[1]))
