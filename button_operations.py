from selenium.webdriver import ActionChains
import driver
import unittest

class buttonOperations(unittest.TestCase):

    def test_button(self):
        if driver.current_test['actionType'] =='click':
            component = driver.global_driver.find_element_by_id(driver.current_test['resourceId'])
            component.click()
        elif driver.current_test['actionType'] =='move':
            component = driver.global_driver.find_element_by_id(driver.current_test['resourceId'])
            actions = ActionChains(driver)
            actions.move_to(component, 10, 10)
            actions.perform()





