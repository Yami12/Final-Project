import unittest
import driver
import time
import ast
from distutils.util import strtobool
import subprocess
from queue import Queue
import re
from read_messaging_logs import AsynchronousFileReader
import xml_parsing
import string_list as sl
import components_operations
logs = []
# app_information = {'WhatsApp': ['com.whatsapp', 'com.whatsapp.HomeActivity t475'],
#                    'Facebook': ['com.facebook.katana', 'com.facebook.katana.activity.FbMainTabActivity'],
#                    'Instagram': ['com.instagram.android', 'com.instagram.mainactivity.MainActivity'],
#                    'Telegram': ['org.telegram.messenger', 'org.telegram.ui.LaunchActivity'],
#                    'Snapchat': ['com.snapchat.android', 'com.snapchat.android.LandingPageActivity']}


class Messaging (unittest.TestCase):
    # A function that checks whether the message sent in a test exists in the list of received logs
    def check_logs(self):
        global logs
        print("-------",logs[0], '_______________________')
        current_test = driver.current_test
        for log in logs:
            specific_log = log.replace("false", "False").replace("true", "True")
            print("7777&", specific_log.split("HttpKeepersLogger: ")[1], "************************")
            logs_dict = ast.literal_eval(specific_log.split("HttpKeepersLogger: ")[1])
            print("*************", logs_dict,"************************")

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

    def return_coordinates_by_resource_id(self, step, parent_name):
        process = subprocess.Popen(['adb','-s', 'emulator-5554' ,'exec-out', 'uiautomator', 'dump', '/dev/tty'],stdout=subprocess.PIPE)  # dump the uiautomator file
        content = str(process.stdout.read())
        splitted_content = re.split("<node", content)
        for node in splitted_content:
            if step[sl.TYPE_STEP] == sl.TYPE_ID:
                if step[sl.ID_STEP] in node:
                    process.kill()
                    return re.search('bounds="\[([0-9]+),([0-9]+)\]',node)
            if step[sl.TYPE_STEP] == sl.TYPE_UIAUTOMATOR:
                if parent_name in node and 'class="android.widget.TextView"' in node:
                    process.kill()
                    return re.search('bounds="\[([0-9]+),([0-9]+)\]', node)


    def child_open_chat_screen(self,s_network):
        # launch the application
        subprocess.run(['adb', '-s', 'emulator-5554', 'shell', 'am', 'start', '-n', s_network[sl.APP_PACKAGE]+"/" + s_network[sl.APP_ACTIVITY]])
        time.sleep(3)
        for step in s_network[sl.STEPS]:
            if step[sl.ACTION_STEP] == sl.ACTION_SEND_KEYS:
                if step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT:
                    return
                subprocess.run(['adb','-s', 'emulator-5554' ,'shell', 'input', 'text', s_network[sl.PARENT_NAME]])
            elif step[sl.ACTION_STEP] == sl.ACTION_CLICK:
                coordinates = self.return_coordinates_by_resource_id(step,s_network[sl.PARENT_NAME])
                print("----",coordinates[1], coordinates[2])
                subprocess.run(['adb', '-s', 'emulator-5554','shell', 'input', 'tap', coordinates[1] , coordinates[2]])
            time.sleep(3)

    def get_keepers_logs(self, s_network):
        global logs
        # get keepers logcats to a PIPE
        #TODO change emulator-5554 to be the child device
        process = subprocess.Popen(['adb', '-s', 'emulator-5554', 'logcat', '-s', 'HttpKeepersLogger'],
                                   stdout=subprocess.PIPE)
        stdout_queue = Queue()
        stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.start()

        self.child_open_chat_screen(s_network)#child reed the message

        # uplaod the keepers logs
        subprocess.run(['adb', '-s', 'emulator-5554','shell', 'am', 'broadcast', '-a', 'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])
        time.sleep(15)
        while not stdout_reader.stopped():  # thequeueisemptyandthethreadterminated
            line = stdout_queue.get()
            if "taggedText"in str(line):
                logs.append(str(line))
        print(self.check_logs())

    def send_message_to_child(self):
        networks = xml_parsing.social_network_xml_to_dictionary(sl.NETWORKS_FILE)
        for network in networks:
            # if network[sl.S_NETWORK_NAME] == driver.current_test[sl.TEST_APP_NAME]:
            #     driver.connect_driver(network[sl.APP_PACKAGE],network[sl.APP_ACTIVITY])# connect the driver
            #     for step in network[sl.STEPS]:
            #         driver.global_tests_result.append(components_operations.component_operation(step))

            self.get_keepers_logs(network)

    def test_manage_message(self):
        self.send_message_to_child()










#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# #Whatsapp
# class WhatsappMessaging(unittest.TestCase):
#
#     def tearDown(self):
#         "Tear down the test"
#         current_sender_driver.quit()
#
#     # def father_read_message(self):
#     #     driver.initialize_child()
#     #     time.sleep(4)
#     #     driver.global_driver_child.find_element_by_id("com.whatsapp:id/menuitem_search").click()
#     #     driver.global_driver_child.find_element_by_id("com.whatsapp:id/search_src_text").send_keys("fa")
#     #     driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().textContains("father")').click()
#
#     def test_send_message(self):
#         global current_sender_driver
#         if driver.current_test['side'] == 'send':
#             current_sender_driver = driver.global_driver_child
#             driver.initialize_child(app_information['WhatsApp'][0], app_information['WhatsApp'][1])
#         else:
#             current_sender_driver = driver.global_driver_father
#             driver.initialize_father(app_information['WhatsApp'][0], app_information['WhatsApp'][1])
#         time.sleep(4)
#         current_sender_driver.find_element_by_id("com.whatsapp:id/menuitem_search").click()
#         current_sender_driver.find_element_by_id("com.whatsapp:id/search_src_text").send_keys(driver.current_test['contact'])
#         current_sender_driver.find_element_by_android_uiautomator('new UiSelector().textContains(driver.current_test["contact"])').click()
#         current_sender_driver.find_element_by_id("com.whatsapp:id/entry").send_keys(driver.current_test['text'])
#         current_sender_driver.find_element_by_id("com.whatsapp:id/send").click()
#         ChildLaunchApplication.get_keepers_logs(app_information['WhatsApp'][0] + '/' + app_information['WhatsApp'][1])
#
#
# #Facebook
# class FacebookMessaging(unittest.TestCase):
#     "Class to run tests against the Chess Free app"
#     def tearDown(self):
#         "Tear down the test"
#         current_sender_driver.quit()
#
#     # def father_read_message(self):
#     #     driver.initialize_child('com.facebook.katana', 'com.facebook.katana.activity.FbMainTabActivity')
#     #     time.sleep(15)
#
#     def test_send_message(self):
#         global current_sender_driver
#         if driver.current_test['side'] == 'send':
#             current_sender_driver = driver.global_driver_child
#             driver.initialize_child(app_information['Facebook'][0], app_information['Facebook'][1])
#         else:
#             current_sender_driver = driver.global_driver_father
#             driver.initialize_father(app_information['Facebook'][0], app_information['Facebook'][1])
#         time.sleep(4)
#         current_sender_driver.find_element_by_android_uiautomator('new UiSelector().descriptionContains("חיפוש בפייסבוק")').click()
#         current_sender_driver.find_element_by_class_name("android.widget.EditText").send_keys("הפרש הבודד")
#         current_sender_driver.find_element_by_class_name("android.view.ViewGroup").click()
#         current_sender_driver.find_element_by_class_name("android.view.ViewGroup").click()
#
#         ChildLaunchApplication.get_keepers_logs(app_information['Facebook'][0] + '/' + app_information['Facebook'][1])
#
# #Instagram
# class InstagramMessaging(unittest.TestCase):
#     "Class to run tests against the Chess Free app"
#     def tearDown(self):
#         "Tear down the test"
#         current_sender_driver.quit()
#
#     # def father_read_message(self):
#     #     driver.initialize_child('com.instagram.android', 'com.instagram.mainactivity.MainActivity')
#     #     time.sleep(4)
#     #     driver.global_driver_child.find_element_by_id("com.instagram.android:id/action_bar_inbox_button").click()
#     #     driver.global_driver_child.find_element_by_id("com.instagram.android:id/search_row").click()
#     #     driver.global_driver_child.find_element_by_id("com.instagram.android:id/search_bar_real_field").send_keys("hprshhbv")
#     #     driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().textContains("hprshhbvdd")').click()
#
#     def test_send_message(self):
#         global current_sender_driver
#         if driver.current_test['side'] == 'send':
#             current_sender_driver = driver.global_driver_child
#             driver.initialize_child(app_information['Instagram'][0], app_information['Instagram'][1])
#         else:
#             current_sender_driver = driver.global_driver_father
#             driver.initialize_father(app_information['Instagram'][0], app_information['Instagram'][1])
#         time.sleep(4)
#         current_sender_driver.find_element_by_android_uiautomator('new UiSelector().descriptionContains("חיפוש וגילוי")').click()
#         name_search_box = current_sender_driver.find_element_by_id("com.instagram.android:id/action_bar_search_edit_text")
#         name_search_box.click()
#         name_search_box.send_keys(driver.current_test["contact"])
#         current_sender_driver.find_element_by_android_uiautomator('new UiSelector().textContains(driver.current_test["contact"])').click()
#         messagge_button_list = current_sender_driver.find_elements_by_class_name("android.widget.TextView")
#         for element in messagge_button_list:
#             if 'הודעה' in str(element.get_attribute("text")):
#                 element.click()
#                 break
#         current_sender_driver.find_element_by_id("com.instagram.android:id/row_thread_composer_edittext").send_keys(driver.current_test['text'])
#         current_sender_driver.find_element_by_id("com.instagram.android:id/row_thread_composer_button_send").click()
#
#         ChildLaunchApplication.get_keepers_logs(app_information['Instagram'][0] + '/' + app_information['Instagram'][1])
#
# #Telegram
# class TelegramMessaging(unittest.TestCase):
#     "Class to run tests against the Chess Free app"
#     def tearDown(self):
#         "Tear down the test"
#         current_sender_driver.quit()
#
#     # def father_read_message(self):
#     #     driver.initialize_child('org.telegram.messenger', 'org.telegram.ui.LaunchActivity')
#     #     time.sleep(4)
#     #     driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().descriptionContains("חיפוש")').click()
#     #     driver.global_driver_child.find_element_by_class_name("android.widget.EditText").send_keys("יחי")
#     #     driver.global_driver_child.find_element_by_android_uiautomator('new UiSelector().textContains("יחיאל")').click()
#
#     def test_send_message(self):
#         global current_sender_driver
#         if driver.current_test['side'] == 'send':
#             current_sender_driver = driver.global_driver_child
#             driver.initialize_child(app_information['Telegram'][0], app_information['Telegram'][1])
#         else:
#             current_sender_driver = driver.global_driver_father
#             driver.initialize_father(app_information['Telegram'][0], app_information['Telegram'][1])
#         time.sleep(4)
#         current_sender_driver.find_element_by_android_uiautomator('new UiSelector().descriptionContains("חיפוש")').click()
#         current_sender_driver.find_element_by_class_name("android.widget.EditText").send_keys(driver.current_test["contact"])
#         current_sender_driver.find_element_by_android_uiautomator('new UiSelector().textContains(driver.current_test["contact"])').click()
#         current_sender_driver.find_element_by_class_name("android.widget.EditText").send_keys(driver.current_test['text'])
#         current_sender_driver.find_element_by_android_uiautomator('new UiSelector().descriptionContains("שלח")').click()
#
#         ChildLaunchApplication.get_keepers_logs(app_information['Telegram'][0] + '/' + app_information['Telegram'][1])
#
# #Snapchat
# class SnapchatMessage(unittest.TestCase):
#     def tearDown(self):
#         "Tear down the test"
#         current_sender_driver.quit()
#
#     # def father_read_message(self):
#     #     driver.initialize_child('com.snapchat.android', 'com.snapchat.android.LandingPageActivity')
#     #     time.sleep(15)
#
#     def test_send_message(self):
#         global current_sender_driver
#         if driver.current_test['side'] == 'send':
#             current_sender_driver = driver.global_driver_child
#             driver.initialize_child(app_information['Snapchat'][0], app_information['Snapchat'][1])
#         else:
#             current_sender_driver = driver.global_driver_father
#             driver.initialize_father(app_information['Snapchat'][0], app_information['Snapchat'][1])
#         time.sleep(4)
#         current_sender_driver.find_element_by_id('com.snapchat.android:id/neon_header_title').click()
#         # time.sleep(10)
#        # name_search_box = driver.global_driver_father.find_element_by_id("com.snapchat.android:id/neon_header_layout")
#
#         #search_button.send_keys("ch")
#         print("----1")
#         current_sender_driver.find_element_by_class_name('android.widget.EditText').send_keys("ch")
#         print("----2")
#
#         ChildLaunchApplication.get_keepers_logs(app_information['Snapchat'][0] + '/' + app_information['Snapchat'][1])
#
#
# class checkAlertMessageFatherSide(unittest.TestCase):
#
#     def tearDown(self):
#         "Tear down the test"
#         driver.global_driver_father.quit()
#
#     def test_check_alert_message(self):
#         driver.initialize_father("", "")
#         time.sleep(10)
#
# print(ChildLaunchApplication.check_logs(ChildLaunchApplication))