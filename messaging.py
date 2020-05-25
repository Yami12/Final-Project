import unittest
import driver
import time
import ast
from distutils.util import strtobool
import subprocess
import datetime
from read_messaging_logs import AsynchronousFileReader
from queue import Queue
import re
from read_messaging_logs import AsynchronousFileReader

logs = []
app_information = {'WhatsApp': ['com.whatsapp', 'com.whatsapp.HomeActivity t475'],
                   'Facebook': ['com.facebook.katana', 'com.facebook.katana.activity.FbMainTabActivity'],
                   'Instagram': ['com.instagram.android', 'com.instagram.mainactivity.MainActivity'],
                   'Telegram': ['org.telegram.messenger', 'org.telegram.ui.LaunchActivity'],
                   'Snapchat': ['com.snapchat.android', 'com.snapchat.android.LandingPageActivity']}

class ChildLaunchApplication():

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_child.quit()

    def enter_contact_conversation(self):
        subprocess.run(['adb', 'shell', 'uiautomator', 'dump']) # dump the uiautomator file
        process = subprocess.Popen(['adb', 'shell', 'cat', '/sdcard/window_dump.xml'],
                                   stdout=subprocess.PIPE) # write the content file to the pipe

        content = str(process.stdout.read())
        splitted_content = re.split("bounds", content)
        for item in splitted_content:
            if "conversations_row_contact_name" in item:
                coordinates = re.search("(\[[0-9].*\[)",item)[1][:-1]
                splitted_coordinates = re.split('[\[,\]]',coordinates)
                subprocess.run(['adb', 'shell', 'input', 'tap', splitted_coordinates[1], splitted_coordinates[2]])
                process.kill()

    #A function that checks whether the message sent in a test exists in the list of received logs
    def check_logs(self):
        global logs
        current_test = driver.current_test
        for log in logs:
            specific_log = log.replace("false", "False").replace("true", "True")
            logs_dict = ast.literal_eval(specific_log)
            if logs_dict['applicationName'] == current_test['application']:
                if logs_dict['isGroup'] == strtobool(current_test['isGroup']):
                    if logs_dict['title'] == current_test['contact']:
                        messages = logs_dict['messages']
                        for message in messages:
                            if (message['isOutgoing'] == True and current_test['side'] == 'recive') or (
                                    message['isOutgoing'] == False and current_test['side'] == 'send'):
                                if message['taggedText'] == current_test['text']:
                                    return True
        return False


    def launch_application_screen(self, app_package):
        # launch the application
        subprocess.run(['adb', 'shell', 'am', 'start', '-n', app_package])
        # click the 'search' button
        subprocess.run(['adb', 'shell', 'input', 'keyevent', '84'])
        # write the contact name
        subprocess.run(['adb', 'shell', 'input', 'text', 'Father'])
        # enter the contact conversation
        ChildLaunchApplication.enter_contact_conversation()
        time.sleep(15)


    def get_keepers_logs(self, app_package):
        # get keepers logcats to a PIPE
        process = subprocess.Popen(['adb', '-s', 'emulator-5554', 'logcat', '-s', 'HttpKeepersLogger'],
                                   stdout=subprocess.PIPE)
        stdout_queue = Queue()
        stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.start()

        ChildLaunchApplication.launch_application_screen(app_package)#child reed the message

        # uplaod the keepers logs
        subprocess.run(['adb', 'shell', 'am', 'broadcast', '-a', 'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])
        time.sleep(15)
        # TODO check how to kill thread, how to check thatthe queu is empty and remove the break and replace the while condition
        while (True):
            line = stdout_queue.get()
            if "taggedText" in str(line):
                logs.append(str(line))
                print(logs)
                break

        result = ChildLaunchApplication.check_logs()
        #TODO add the result to results


#Whatsapp
class WhatsappMessaging(unittest.TestCase):

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def father_read_message(self):
        driver.initialize_child()
        time.sleep(4)
        driver.global_driver_child.find_element_by_id("com.whatsapp:id/menuitem_search").click()
        driver.global_driver_child.find_element_by_id("com.whatsapp:id/search_src_text").send_keys("fa")
        driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().textContains("father")').click()

    def test_send_message(self):
        if driver.current_test['side'] == 'send':
            driver.initialize_child(app_information['WhatsApp'][0], app_information['WhatsApp'][1])
        else:
            driver.initialize_father(app_information['WhatsApp'][0], app_information['WhatsApp'][1])
        time.sleep(4)
        driver.global_driver_father.find_element_by_id("com.whatsapp:id/menuitem_search").click()
        driver.global_driver_father.find_element_by_id("com.whatsapp:id/search_src_text").send_keys(driver.current_test['contact'])
        driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().textContains(driver.current_test["contact"])').click()
        driver.global_driver_father.find_element_by_id("com.whatsapp:id/entry").send_keys(driver.current_test['text'])
        driver.global_driver_father.find_element_by_id("com.whatsapp:id/send").click()
        ChildLaunchApplication.get_keepers_logs(app_information['WhatsApp'][0] + '/' + app_information['WhatsApp'][1])


#Facebook
class FacebookMessaging(unittest.TestCase):
    "Class to run tests against the Chess Free app"
    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def father_read_message(self):
        driver.initialize_child('com.facebook.katana', 'com.facebook.katana.activity.FbMainTabActivity')
        time.sleep(15)

    def test_send_message(self):
        if driver.current_test['side'] == 'send':
            driver.initialize_child(app_information['Facebook'][0], app_information['Facebook'][1])
        else:
            driver.initialize_father(app_information['Facebook'][0], app_information['Facebook'][1])
        time.sleep(4)
        driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().descriptionContains("חיפוש בפייסבוק")').click()
        driver.global_driver_father.find_element_by_class_name("android.widget.EditText").send_keys("הפרש הבודד")
        driver.global_driver_father.find_element_by_class_name("android.view.ViewGroup").click()
        driver.global_driver_father.find_element_by_class_name("android.view.ViewGroup").click()

        ChildLaunchApplication.get_keepers_logs(app_information['Facebook'][0] + '/' + app_information['Facebook'][1])

#Instagram
class InstagramMessaging(unittest.TestCase):
    "Class to run tests against the Chess Free app"
    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def father_read_message(self):
        driver.initialize_child('com.instagram.android', 'com.instagram.mainactivity.MainActivity')
        time.sleep(4)
        driver.global_driver_child.find_element_by_id("com.instagram.android:id/action_bar_inbox_button").click()
        driver.global_driver_child.find_element_by_id("com.instagram.android:id/search_row").click()
        driver.global_driver_child.find_element_by_id("com.instagram.android:id/search_bar_real_field").send_keys("hprshhbv")
        driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().textContains("hprshhbvdd")').click()

    def test_send_message(self):
        if driver.current_test['side'] == 'send':
            driver.initialize_child(app_information['Instagram'][0], app_information['Instagram'][1])
        else:
            driver.initialize_father(app_information['Instagram'][0], app_information['Instagram'][1])
        time.sleep(4)
        driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().descriptionContains("חיפוש וגילוי")').click()
        name_search_box = driver.global_driver_father.find_element_by_id("com.instagram.android:id/action_bar_search_edit_text")
        name_search_box.click()
        name_search_box.send_keys(driver.current_test["contact"])
        driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().textContains(driver.current_test["contact"])').click()
        messagge_button_list = driver.global_driver_father.find_elements_by_class_name("android.widget.TextView")
        for element in messagge_button_list:
            if 'הודעה' in str(element.get_attribute("text")):
                element.click()
                break
        driver.global_driver_father.find_element_by_id("com.instagram.android:id/row_thread_composer_edittext").send_keys(driver.current_test['text'])
        driver.global_driver_father.find_element_by_id("com.instagram.android:id/row_thread_composer_button_send").click()

        ChildLaunchApplication.get_keepers_logs(app_information['Instagram'][0] + '/' + app_information['Instagram'][1])

#Telegram
class TelegramMessaging(unittest.TestCase):
    "Class to run tests against the Chess Free app"
    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def father_read_message(self):
        driver.initialize_child('org.telegram.messenger', 'org.telegram.ui.LaunchActivity')
        time.sleep(4)
        driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().descriptionContains("חיפוש")').click()
        driver.global_driver_child.find_element_by_class_name("android.widget.EditText").send_keys("יחי")
        driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().textContains("יחיאל")').click()


    def test_send_message(self):
        if driver.current_test['side'] == 'send':
            driver.initialize_child(app_information['Telegram'][0], app_information['Telegram'][1])
        else:
            driver.initialize_father(app_information['Telegram'][0], app_information['Telegram'][1])
        time.sleep(4)
        driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().descriptionContains("חיפוש")').click()
        driver.global_driver_father.find_element_by_class_name("android.widget.EditText").send_keys(driver.current_test["contact"])
        driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().textContains(driver.current_test["contact"])').click()
        driver.global_driver_father.find_element_by_class_name("android.widget.EditText").send_keys(driver.current_test['text'])
        driver.global_driver_father.find_element_by_android_uiautomator('new UiSelector().descriptionContains("שלח")').click()

        ChildLaunchApplication.get_keepers_logs(app_information['Telegram'][0] + '/' + app_information['Telegram'][1])

#Snapchat
class SnapchatMessage(unittest.TestCase):
    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def father_read_message(self):
        driver.initialize_child('com.snapchat.android', 'com.snapchat.android.LandingPageActivity')
        time.sleep(15)

    def test_send_message(self):
        if driver.current_test['side'] == 'send':
            driver.initialize_child(app_information['Snapchat'][0], app_information['Snapchat'][1])
        else:
            driver.initialize_father(app_information['Snapchat'][0], app_information['Snapchat'][1])
        time.sleep(4)
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

        ChildLaunchApplication.get_keepers_logs(app_information['Snapchat'][0] + '/' + app_information['Snapchat'][1])


class checkAlertMessageFatherSide(unittest.TestCase):

    def tearDown(self):
        "Tear down the test"
        driver.global_driver_father.quit()

    def test_check_alert_message(self):
        driver.initialize_father("", "")
        time.sleep(10)

print(ChildLaunchApplication.check_logs(ChildLaunchApplication))