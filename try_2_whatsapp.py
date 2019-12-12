import os
import unittest
from appium import webdriver
from time import sleep


class WhatsappAndroidTests(unittest.TestCase):
    "Class to run tests against the Chess Free app"

    def setUp(self):
        "Setup for the test"
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8.0.0'
        desired_caps['deviceName'] = 'My HUAWEI'
        desired_caps['noReset'] = 'true'
        # Returns abs path relative to this file and not cwd
        desired_caps['appPackage'] = 'com.whatsapp'
        desired_caps['appActivity'] = 'com.whatsapp.HomeActivity t475'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        "Tear down the test"
        self.driver.quit()

    def test_text_friend(self):
        "Test the Chess app launches correctly and click on Play button"
        search_button = self.driver.find_element_by_id("com.whatsapp:id/menuitem_search")
        search_button.click()

        name_search_box = self.driver.find_element_by_id("com.whatsapp:id/search_src_text")
        name_search_box.send_keys("תהי")

        msg= self.driver.find_element_by_android_uiautomator('new UiSelector().textContains("תהילה")')
        msg.click()

        text_box = self.driver.find_element_by_id("com.whatsapp:id/entry")
        text_box.send_keys("Testing...")

        send_button = self.driver.find_element_by_id("com.whatsapp:id/send")
        send_button.click()

        time.sleep(20)



# ---START OF SCRIPT
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(WhatsappAndroidTests)
    unittest.TextTestRunner(verbosity=1).run(suite)
