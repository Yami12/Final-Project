import unittest
import driver
from time import sleep


class DownloadApp(unittest.TestCase):
    "Class to run tests against the Chess Free app"

    def test_a_install(self):
        "Test the Chess app launches correctly and click on Play button"
        driver.global_driver.is_app_installed('com.keepers')

    def test_b_features_screams(self):
        sleep(6)
        start_onboarding_button = driver.global_driver.find_element_by_id("com.keepers:id/start_onboarding_button")
        start_onboarding_button.click()
        start_onboarding_button.click()
        start_onboarding_button.click()
        start_onboarding_button.click()
        start_onboarding_button.click()
        start_onboarding_button.click()
        start_onboarding_button.click()

