import unittest
from time import sleep
import components_operations
import driver

class InstallChildSide(unittest.TestCase):
    "Class to run tests against the Chess Free app"


    def test_a_install_child_side(self):
        sleep(6)
        components_operations.button_click("com.keepers:id/check_i_accept")
        components_operations.button_click("com.keepers:id/activity_terms_child_button")
        sleep(6)
        components_operations.input_send_keys("com.keepers:id/input_child_name", "ימי")
        components_operations.input_send_keys("com.keepers:id/input_date_of_birth", "1.1.2010")
        components_operations.input_send_keys("com.keepers:id/input_email", "yechialmiller@gmail.com")
        components_operations.input_send_keys("com.keepers:id/input_password", "ym754321")

        driver.global_driver.hide_keyboard()
        components_operations.button_click("com.keepers:id/button_proceed")

        sleep(5)
        #country_name = self.driver.find_element_by_id("com.keepers:id/countries")
        # country_name =driver.global_driver.find_element_by_xpath("//*[@resource-id = 'com.keepers:id/countries' and @index ='1']")
        # country_name.click()
        sleep(5)
        components_operations.button_click("com.keepers:id/button_proceed")


