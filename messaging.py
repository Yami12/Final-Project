import unittest
import driver
import time
import subprocess
import datetime
from read_messaging_logs import AsynchronousFileReader

from queue import Queue

class OpenChildSideApplication(unittest.TestCase):

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_child.quit()

    def test_open_application_screen(self):
        driver.initialize_child('com.keepers', 'com.keeper.common.splash.SplashActivity')
        time.sleep(10)

#Whatsapp
class FatherSendWhatsappMessage(unittest.TestCase):
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
        driver.initialize_father('com.whatsapp', 'com.whatsapp.HomeActivity t475')
        time.sleep(10)
        search_button = driver.global_driver_father.find_element_by_id("com.whatsapp:id/menuitem_search")
        search_button.click()
        name_search_box = driver.global_driver_father.find_element_by_id("com.whatsapp:id/search_src_text")
        name_search_box.send_keys("יח")
        msg = driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().textContains("יחיאל כשר")')
        msg.click()
        text_box = driver.global_driver_father.find_element_by_id("com.whatsapp:id/entry")
        text_box.send_keys(driver.current_test['text'])
        send_button = driver.global_driver_father.find_element_by_id("com.whatsapp:id/send")
        send_button.click()
        time.sleep(20)
        # WhatsappMessage.child_read_message(self)


class ChildReadWhatsappMessage(unittest.TestCase):
    #
    # def tearDown(self):
    #     "Tear down the test"
    #     driver.global_driver_child.quit()

    def test_child_read_message(self):
        # # start read the logcats
        # process = subprocess.Popen(['adb', '-s', 'emulator-5554', 'logcat', '-s', 'HttpKeepersLogger'],
        #                            stdout=subprocess.PIPE)
        #
        # # Launch the asynchronous readers of the process' stdout.
        # stdout_queue = Queue()
        # stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
        # stdout_reader.start()


        print(datetime.datetime.now().time())

        driver.initialize_child('com.whatsapp', 'com.whatsapp.HomeActivity t475')
        time.sleep(10)
        search_button = driver.global_driver_child.find_element_by_id("com.whatsapp:id/menuitem_search")
        search_button.click()
        time.sleep(10)
        name_search_box = driver.global_driver_child.find_element_by_id("com.whatsapp:id/search_src_text")
        name_search_box.send_keys("fa")
        time.sleep(5)
        print("hiii")
        # msg = driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().textContains("father")')
        # msg.click()
        # time.sleep(5)
        # text_box = driver.global_driver_child.find_element_by_id("com.whatsapp:id/entry")
        # text_box.send_keys('I read')
        # send_button = driver.global_driver_child.find_element_by_id("com.whatsapp:id/send")
        # send_button.click()
        # time.sleep(10)
        # driver.global_driver_child.close_app()
        # time.sleep(20)
        # driver.global_driver_child.launch_app()
        # time.sleep(5)
        # driver.global_driver_child.launch_app()
        # time.sleep(5)
        # search_button = driver.global_driver_child.find_element_by_id("com.whatsapp:id/menuitem_search")
        # search_button.click()
        # time.sleep(10)
        # name_search_box = driver.global_driver_child.find_element_by_id("com.whatsapp:id/search_src_text")
        # name_search_box.send_keys("fa")
        # msg = driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().textContains("father")')
        # msg.click()
        # driver.global_driver_child.hide_keyboard()
        # # subprocess.run(['adb', 'shell', 'am', 'broadcast', '-a', 'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])
        # # time.sleep(60)

        print(datetime.datetime.now().time())
        # send broadcast
        # subprocess.run(['adb', 'shell', 'am', 'broadcast', '-a', 'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])
        #
        # # print the logcats
        # # while not stdout_reader.eof():
        #     # while not stdout_queue.empty():
        # while (1):
        #     while(1):
        #         line = stdout_queue.get()
        #         # if "taggedText" in str(line):
        #         print(line)

        # time.sleep(10)


#Facebook
class FatherSendFacebookMessage(unittest.TestCase):
    "Class to run tests against the Chess Free app"
    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def test_father_send_message(self):
        driver.initialize_father('com.facebook.katana', 'com.facebook.katana.activity.FbMainTabActivity')
        time.sleep(10)


class ChildReadFacebookMessage(unittest.TestCase):

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_child.quit()

    def test_child_read_message(self):
        driver.initialize_child('com.facebook.katana', 'com.facebook.katana.activity.FbMainTabActivity')
        time.sleep(15)


#Instagram
class FatherSendInstagramMessage(unittest.TestCase):
    "Class to run tests against the Chess Free app"
    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def test_father_send_message(self):
        driver.initialize_father('com.instagram.android', 'com.instagram.mainactivity.MainActivity')
        time.sleep(10)
        search_button = driver.global_driver_father.find_element_by_id('com.instagram.android:id/tab_icon')
        search_button.click()
        time.sleep(10)
        name_search_box = driver.global_driver_father.find_element_by_id("com.instagram.android:id/action_bar_search_edit_text")
        name_search_box.send_keys("hprshhbv")
        msg = driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().textContains("hprshhbvdd")')
        msg.click()


class ChildReadInstagramMessage(unittest.TestCase):

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_child.quit()

    def test_child_read_message(self):
        driver.initialize_child('com.instagram.android', 'com.instagram.mainactivity.MainActivity')
        time.sleep(15)


#Telegram
class FatherSendTelegramMessage(unittest.TestCase):
    "Class to run tests against the Chess Free app"
    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def test_father_send_message(self):
        driver.initialize_father('org.telegram.messenger', 'org.telegram.ui.LaunchActivity')
        time.sleep(10)
        search_button = driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().descriptionContains("חיפוש")')
        search_button.click()
        time.sleep(10)
        name_search_box = driver.global_driver_father.find_element_by_xpath("//div[contains(text(),'חיפוש')]")
        name_search_box.send_keys("יחי")

class ChildReadTelegramMessage(unittest.TestCase):

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_child.quit()

    def test_child_read_message(self):
        driver.initialize_child('org.telegram.messenger', 'org.telegram.ui.LaunchActivity')
        time.sleep(15)


#Snapchat
class FatherSendSnapchatMessage(unittest.TestCase):
    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def test_father_send_message(self):
        driver.initialize_father('com.snapchat.android', 'com.snapchat.android.LandingPageActivity')
        time.sleep(10)
        search_button = driver.global_driver_father.find_element_by_id('com.snapchat.android:id/neon_header_title')
        search_button.click()
        # time.sleep(10)
       # name_search_box = driver.global_driver_father.find_element_by_id("com.snapchat.android:id/neon_header_layout")

        #search_button.send_keys("ch")
        print("----1")
        msg = driver.global_driver_father.find_element_by_class_name('android.widget.EditText')
        print("----3")
        msg.send_keys("ch")
        print("----2")

class ChildReadSnapchatMessage(unittest.TestCase):

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_child.quit()

    def test_child_read_message(self):
        driver.initialize_child('com.snapchat.android', 'com.snapchat.android.LandingPageActivity')
        time.sleep(15)



class CheckChildLogs(unittest.TestCase):
    def tearDown(self):
        "Tear down the test"
        driver.global_driver_child.quit()

    def test_capture_logcat(self):
       " you should use here main_tester.logs"


class checkAlertMessageFatherSide(unittest.TestCase):

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def test_check_alert_message(self):
        driver.initialize_father("", "")
        time.sleep(10)