import unittest
from time import sleep
import driver

class InstallChildSide(unittest.TestCase):
    "Class to run tests against the Chess Free app"

    def setUp(self):
        self.driver = driver.global_driver

    def tearDown(self):
        "Tear down the test"
        self.driver.quit()


    def test_a_install_child_side(self):
        sleep(6)
        check_i_accept = self.driver.find_element_by_id("com.keepers:id/check_i_accept")
        check_i_accept.click()

        child_button = self.driver.find_element_by_id("com.keepers:id/activity_terms_child_button")
        child_button.click()
        sleep(6)
        child_name_input = self.driver.find_element_by_id("com.keepers:id/input_child_name")
        child_name_input.send_keys("ימי")

        date_of_birth_input = self.driver.find_element_by_id("com.keepers:id/input_date_of_birth")
        date_of_birth_input.send_keys("1.1.2010")

        email_input = self.driver.find_element_by_id("com.keepers:id/input_email")
        email_input.send_keys("yechialmiller@gmail.com")

        password_input = self.driver.find_element_by_id("com.keepers:id/input_password")
        password_input.send_keys("ym754321")

        self.driver.hide_keyboard()
        button_proceed = self.driver.find_element_by_id("com.keepers:id/button_proceed")
        button_proceed.click()

        print("succeeded to install level 2")
        sleep(5)
        #country_name = self.driver.find_element_by_id("com.keepers:id/countries")
        country_name = self.driver.find_element_by_xpath("//*[@resource-id = 'com.keepers:id/countries' and @index ='1']")
        country_name.click()
        sleep(5)
        button_proceed = self.driver.find_element_by_id("com.keepers:id/button_proceed")
        button_proceed.click()

