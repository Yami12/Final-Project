import driver
import unittest
from time import sleep

class inpoutOperations(unittest.TestCase):

    def test_input(self):
        sleep(3)
        print(driver.current_test['resourceId'])
        input = driver.global_driver.find_element_by_id(driver.current_test['resourceId'])
        input.send_keys(driver.current_test['content'])