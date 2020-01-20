from selenium.webdriver import ActionChains
import driver
import unittest
import re

class buttonOperations(unittest.TestCase):

    #
    #Checks whether the result matches the expected result
    #
    def check_expected_result(self):
        error_message = ''
        error_message_text = ''
        if re.search("toastMessage:.*", driver.current_test['expectedResult']):# taost message
            error_message = driver.global_driver.find_element_by_xpath("//android.widget.Toast[1]")
            error_message_text = error_message.get_attribute("text")
        if re.search("labelMessage:.*", driver.current_test['expectedResult']):# label message
            error_message = driver.global_driver.find_element_by_id('com.keepers:id/textinput_error')
            error_message_text = error_message.get_attribute("text")
        print(error_message_text)
        if error_message_text != '' and error_message_text != driver.current_test['expectedResult'].split(':')[1]:
            return -1

    #
    # Handle button operations
    #
    def test_button(self):
        if driver.current_test['actionType'] =='click':#click operation
            component = driver.global_driver.find_element_by_id(driver.current_test['resourceId'])
            component.click()
            buttonOperations.check_expected_result(self)
        elif driver.current_test['actionType'] =='over':#move operation
            component = driver.global_driver.find_element_by_id(driver.current_test['resourceId'])
            actions = ActionChains(driver)
            actions.move_to(component, 10, 10)
            actions.perform()
            buttonOperations.check_expected_result(self)





