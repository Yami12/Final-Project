
import unittest
import driver
import time


class FatherSentWhatsappMessage(unittest.TestCase):
    "Class to run tests against the Chess Free app"

    # def setUp(self):
    #     "Setup for the test"
    #     desired_caps = {}
    #     desired_caps['platformName'] = 'Android'
    #     desired_caps['platformVersion'] = '8.0.0'
    #     desired_caps['deviceName'] = 'My HUAWEI'
    #     desired_caps['noReset'] = 'true'
    #     # Returns abs path relative to this file and not cwd
    #     desired_caps['appPackage'] = 'com.whatsapp'
    #     desired_caps['appActivity'] = 'com.whatsapp.HomeActivity t475'
    #     self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def test_father_send_message(self):
        print("yay 2")
        driver.initialize_father()
        print("yay 3")
        time.sleep(5)
        search_button = driver.global_driver_father.find_element_by_id("com.whatsapp:id/menuitem_search")
        search_button.click()

        name_search_box = driver.global_driver_father.find_element_by_id("com.whatsapp:id/search_src_text")
        name_search_box.send_keys("ch")

        msg= driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().textContains("child")')
        msg.click()

        text_box = driver.global_driver_father.find_element_by_id("com.whatsapp:id/entry")
        text_box.send_keys(driver.current_test['text'])

        send_button = driver.global_driver_father.find_element_by_id("com.whatsapp:id/send")
        send_button.click()


        time.sleep(20)
        # WhatsappMessage.child_read_message(self)



class ChildReadWhatsappMessage(unittest.TestCase):

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_child.quit()

    def test_child_read_message(self):
        driver.initialize_child()
        time.sleep(15)
        search_button = driver.global_driver_child.find_element_by_id("com.whatsapp:id/menuitem_search")
        search_button.click()
        time.sleep(10)

        name_search_box = driver.global_driver_child.find_element_by_id("com.whatsapp:id/search_src_text")
        name_search_box.send_keys("fa")

        msg = driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().textContains("father")')
        msg.click()

        time.sleep(10)




class CheckChildLogs(unittest.TestCase):
    def tearDown(self):
        "Tear down the test"
        driver.global_driver_child.quit()

    def test_capture_logcat(self):
        time.sleep(30)
        driver.initialize_child()
        # inspect available log types
        logtypes = driver.global_driver_child.log_types
        print(' ,'.join(logtypes))  #

        # print first and last 10 lines of logs
        logs = driver.global_driver_child.get_log('logcat')
        print("log structure:",logs[0])
        log_messages = list(map(lambda log: log['message'], logs))
        for log in log_messages:
            if 'HttpKeepersLogger'in log:
                print(log)
                print("----------------------------------------")
        # print('First and last ten lines of log: ')
        # print('\n'.join(log_messages[:10]))
        # print('...')
        # print('\n'.join(log_messages[-9:]))

        # wait for more logs
        time.sleep(10)

        # demonstrate that each time get logs, we only get new logs
        # which were generated since the last time we got logs
        logs = driver.global_driver_child.get_log('logcat')
        second_set_of_log_messages = list(map(lambda log: log['message'], logs))
        for log in log_messages:
            if 'HttpKeepersLogger' in log:
                print(log)
                print("----------------------------------------")




