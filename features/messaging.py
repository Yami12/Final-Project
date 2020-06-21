import unittest
import datetime
import time
import ast
from distutils.util import strtobool
import subprocess
from queue import Queue
import re
from utils import utils_funcs

from utils import driver
from utils import read_messaging_logs
from utils import xml_parsing
from utils import string_list as sl

from components import components_operations

logs = []


class Messaging (unittest.TestCase):
    # A function that checks whether the message sent in a test exists in the list of received logs
    def check_messaging_logs(self, logs_dict, chat_name):
        current_test = driver.current_test
        if logs_dict['applicationName'] == current_test['application']:
            if logs_dict['isGroup'] == strtobool(current_test['isGroup']):
                if logs_dict['title'] == chat_name:
                    messages = logs_dict['messages']
                    for message in messages:
                        if (message['isOutgoing'] == True and current_test['side'] == 'send') or (
                                message['isOutgoing'] == False and current_test['side'] == 'recive'):
                            if message['taggedText'] == current_test['text']:
                                if utils_funcs.time_in_range(message['timeReceived'], 1) == True:
                                    return True
        return False

    def check_parent_logs(self, parent_name):
        # get keepers logcats to a PIPE
        process = subprocess.Popen(['adb', '-s', driver.father_device, 'logcat', '-s', 'HttpKeepersLogger'],
                                   stdout=subprocess.PIPE)
        stdout_queue = Queue()
        stdout_reader = read_messaging_logs.AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.start()

        time.sleep(2)
        stdout_queue.clear()
        while stdout_queue.empty():
            continue
        time.sleep(2)

        parent_logs = ""
        start_dict = False
        while not stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = stdout_queue.get()
            if "{" in line:
                start_dict = True
            if start_dict == True:
                parent_logs = parent_logs + line.split("HttpKeepersLogger: ")[1].split("\n")[0]
            if ": }" in line:
                start_dict = False
            print("parent log: ", parent_logs)
            specific_log = parent_logs.replace("false", "False").replace("true", "True")
            logs_dict = ast.literal_eval(specific_log)
            print("logs_dict: ", logs_dict)
            log_exist = self.check_messaging_logs(logs_dict, parent_name)
            if log_exist == True:
                driver.global_tests_result.append(['True', logs_dict])
                return
        driver.global_tests_result.append(['False', "No logs received"])
        print("False")


    def check_child_logs(self, parent_name):
        global logs
        print("logs: ", logs)

        for log in logs:
            print("log: ", log)
            specific_log = log.replace("false", "False").replace("true", "True")
            specific_log = specific_log.split("HttpKeepersLogger: ")[1]
            specific_log = specific_log.split("\\r\\n")[0]
            print("specific log: ", specific_log)
            logs_dict = ast.literal_eval(specific_log)
            print("log_dict: ", logs_dict)
            log_exist = self.check_messaging_logs(logs_dict, parent_name)
            if log_exist == True:
                driver.global_tests_result.append(['True', logs_dict])
                return
        driver.global_tests_result.append(['False', "No logs received"])
        print("False")

    def check_remove_group_logs(self):
        global logs
        print("logs: ", logs)
        current_test = driver.current_test

        for log in logs:
            specific_log = log.replace("false", "False").replace("true", "True")
            specific_log = specific_log.split("HttpKeepersLogger: ")[1]
            specific_log = specific_log.split("\\r\\n")[0]
            logs_dict = ast.literal_eval(specific_log)

            if logs_dict['eventData'] == current_test[sl.CHAT_NAME] and "CHILD_REMOVED_FROM" in logs_dict['eventType']:
                driver.global_tests_result.append(['True', logs_dict])
                print(['True', logs_dict])
                return True

        driver.global_tests_result.append(['False', "No logs received"])
        print(['False', "No logs received"])
        return False

    def return_coordinates_by_resource_id(self, step, parent_name):
        process = subprocess.Popen(['adb','-s', driver.child_device ,'exec-out', 'uiautomator', 'dump', '/dev/tty'],stdout=subprocess.PIPE)  # dump the uiautomator file
        content = str(process.stdout.read())
        print(content)
        splitted_content = re.split("<node", content)
        print(step)
        for node in splitted_content:
            print(node)
            if step[sl.TYPE_STEP] == sl.TYPE_ID and step[sl.ID_STEP] in node: # id

                process.kill()
                return re.search('bounds="\[([0-9]+),([0-9]+)\]',node)
            elif step[sl.TYPE_STEP] == sl.TYPE_UIAUTOMATOR and 'class="android.widget.ImageView"' not in node:
                if step[sl.CONTENT_STEP] == sl.CHAT_NAME:
                    if parent_name in node:
                        process.kill()
                        return re.search('bounds="\[([0-9]+),([0-9]+)\]', node)
                elif 'content-desc="' + step[sl.CONTENT_STEP] in node:
                    process.kill()
                    return re.search('bounds="\[([0-9]+),([0-9]+)\]', node)


            elif step[sl.TYPE_STEP] == sl.TYPE_CLASS and 'class="' + step[sl.ID_STEP] in node: # class
                process.kill()
                return re.search('bounds="\[([0-9]+),([0-9]+)\]', node)



    def child_open_chat_screen(self, s_network, from_child):
        # launch the application
        print(s_network[sl.APP_PACKAGE]+"/" + s_network[sl.APP_ACTIVITY])
        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'start', '-n', s_network[sl.APP_PACKAGE]+"/" + s_network[sl.APP_ACTIVITY]])
        time.sleep(3)
        for step in s_network[sl.STEPS]:
            if step[sl.ACTION_STEP] == sl.ACTION_SEND_KEYS :
                if step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT and from_child == True:
                    driver.sending_time = datetime.datetime.now()  # save the sending time
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text', driver.current_test[sl.MESSAGING_CONTENT]])
                elif step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT and from_child == False:
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'keyevent', '111'])
                    return
                else:
                    subprocess.run(['adb', '-s', driver.child_device ,'shell', 'input', 'text', driver.current_test[sl.CHAT_NAME][:-1]])
            elif step[sl.ACTION_STEP] == sl.ACTION_CLICK:
                coordinates = self.return_coordinates_by_resource_id(step,s_network[sl.PARENT_NAME])
                subprocess.run(['adb', '-s', driver.child_device,'shell', 'input', 'tap', coordinates[1] , coordinates[2]])
            time.sleep(3)


    def get_keepers_logs(self, s_network, from_child = False):
        device = driver.child_device
        global logs

        # get keepers logcats to a PIPE
        process = subprocess.Popen(['adb', '-s', device, 'logcat', '-s', 'HttpKeepersLogger'],
                                   stdout=subprocess.PIPE)
        stdout_queue = Queue()
        stdout_reader = read_messaging_logs.AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.start()

        self.child_open_chat_screen(s_network, from_child)#child reed the message

        # uplaod the keepers logs
        subprocess.run(['adb', '-s', device,'shell', 'am', 'broadcast', '-a', 'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])
        time.sleep(15)
        while not stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = stdout_queue.get()
            print(line)
            if driver.current_test[sl.TEST_NAME] == sl.REMOVEAL_TEST:
                if "eventType" in str(line):
                    logs.append(str(line))
            else:
                if "taggedText" in str(line):
                    logs.append(str(line))

        if driver.current_test[sl.TEST_NAME] == sl.REMOVEAL_TEST:
            self.check_remove_group_logs()
        else:
            self.check_child_logs(s_network[sl.PARENT_NAME])
            self.check_parent_logs(s_network[sl.PARENT_NAME])


    def send_message(self, from_child=False):
        networks = xml_parsing.tests_xml_to_dictionary(sl.NETWORKS_FILE)
        for network in networks:
            if network[sl.S_NETWORK_NAME] == driver.current_test[sl.TEST_APP_NAME]:
                if driver.current_test[sl.TEST_SIDE] == sl.TEST_RECIVE_SIDE:
                    driver.current_test[sl.CHAT_NAME] = network[sl.CHILD_NAME]
                else:
                    driver.current_test[sl.CHAT_NAME] = network[sl.PARENT_NAME]
                if from_child == False: # send a message to the child
                    driver.connect_driver(network[sl.APP_PACKAGE],network[sl.APP_ACTIVITY])# connect the driver
                    for step in network[sl.STEPS]:
                        driver.global_tests_result.append(components_operations.component_operation(step))

                self.get_keepers_logs(network, from_child)


    def remove_from_group(self):
        networks = xml_parsing.tests_xml_to_dictionary(sl.NETWORKS_FILE)
        removal_networks = xml_parsing.tests_xml_to_dictionary(sl.REMOVAL_FILE)
        current_network = None

        for removal_network in removal_networks:
            if removal_network[sl.S_NETWORK_NAME] == driver.current_test[sl.TEST_APP_NAME]:
                driver.current_test[sl.CHAT_NAME] = removal_network[sl.GROUP_NAME]
                for network in networks:
                    if network[sl.S_NETWORK_NAME] == driver.current_test[sl.TEST_APP_NAME]:
                        current_network = network
                        driver.current_test[sl.CHILD_NAME] = network[sl.CHILD_NAME]
                        driver.connect_driver(network[sl.APP_PACKAGE], network[sl.APP_ACTIVITY])  # connect the driver
                        for step in network[sl.STEPS]:
                            if step[sl.CONTENT_STEP] == 'text':
                                break
                            driver.global_tests_result.append(components_operations.component_operation(step))
                        break
                for step in removal_network[sl.STEPS]:
                    driver.global_tests_result.append(components_operations.component_operation(step))
                break
        self.get_keepers_logs(current_network, False)

    def test_manage_message(self):
        if driver.current_test[sl.TEST_NAME] == 'Removal from group':  # removal from group test
            self.remove_from_group()
        elif driver.current_test[sl.TEST_SIDE] == sl.TEST_RECIVE_SIDE:
            self.send_message()
        elif driver.current_test[sl.TEST_SIDE] == sl.TEST_SEND_SIDE:
            self.send_message(True)


