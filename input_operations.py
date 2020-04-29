'''
This file handles the input resource operations
'''

import driver
import unittest
from time import sleep
import re
from datetime import datetime
class inpoutOperations(unittest.TestCase):
    '''
           function:check_expected_result
           description: checks if the result of the operation is the same as the test's expected result
    '''

    def check_expected_result(self):
        error_message = ''
        error_message_text = ''
        if re.search("toastMessage:.*", driver.current_test['expectedResult']):  # taost message
            error_message = driver.global_driver.find_element_by_xpath("//android.widget.Toast[1]")
            error_message_text = error_message.get_attribute("text")
        if re.search("labelMessage:.*", driver.current_test['expectedResult']):  # label message
            error_message = driver.global_driver.find_element_by_id('com.keepers:id/textinput_error')
            error_message_text = error_message.get_attribute("text")
        print(error_message_text)
        if error_message_text != '' and error_message_text != driver.current_test['expectedResult'].split(':')[
            1]:  # the result is not the same as
            return -1

    '''
        function:test_input
        description: run the current test on the input resource in the application
                 all the test's details are taken from the global current_test attribute
    '''
    def test_input(self):
        if driver.global_driver.is_keyboard_shown():# hides the keyboard
            driver.global_driver.hide_keyboard()
        sleep(3)
        #date time picker
        #if driver.current_test['resourceId'] == "com.keepers:id/input_date_of_birth":
            # input = driver.global_driver.find_element_by_id(driver.current_test['resourceId'])  # find the input resource in the
            # driver.global_driver.execute_script("mobile:setDate", '{element: com.keepers:id/input_date_of_birth, year: 2010, monthOfYear: 12, dayOfMonth: 1}')
            # input.send_keys("11.02.2019")
            # day = driver.global_driver.find_element_by_id("android:id/month_view[3]")
            # day.click()
            # year =driver.global_driver.find_element_by_id("android:id/date_picker_header_year")
            # year.click()
            # change = driver.global_driver.find_element_by_text("2009")
            # change.click()
            #
            #
            #
            #
            #
            # month = "Sep"
            # month_ui = driver.find_element_by_xpath("//android.widget.NumberPicker[1]//android.widget.EditText")  # get month
            # month_ui.click()  # select origin month txt
            # month_ori = str(month_ui.get_attribute("text"))  # get origin month txt
            # for i in range(len(month_ori)):  # delete-key click times
            #     driver.press_keycode(67)
            # driver.set_value(month_ui, month)
        # else:
        input = driver.global_driver.find_element_by_id(driver.current_test['resourceId'])#find the input resource in the application
        input.send_keys(driver.current_test['content']) #f ills the input with the given text
        inpoutOperations.check_expected_result(self)# checks the operation result
        #TODO - hundle the date picker:
        # if driver.current_test['resourceId'] == "com.keepers:id/input_date_of_birth":
        #     input = driver.global_driver.find_element_by_id(driver.current_test['resourceId'])
        #     input.click()
        #     date_picker = driver.global_driver.find_element_by_xpath('//XCUIElementTypePickerWheel')
        #     date_picker.set_value(driver.current_test['content'])