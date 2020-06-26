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

    '''
        A function that checks whether the message sent in a test equal to the received logs
    '''
    def check_messaging_logs(self, logs_dict, chat_name, isParent = False):
        current_test = driver.current_test
        print("log dict: ", logs_dict)
        if logs_dict['applicationName'] == current_test['application']:
            print("same app name")
            if logs_dict['isGroup'] == strtobool(current_test['isGroup']):
                print("same is group")
                if logs_dict['title'] == chat_name:
                    print("same title")
                    messages = logs_dict['messages']
                    for message in messages:
                        print("--------",message['isOutgoing'])
                        if not isParent:
                            print("is outgoing----------")
                            if (message['isOutgoing'] == True and current_test['side'] == 'send') or (
                                message['isOutgoing'] == False and current_test['side'] == 'recive'):
                                print("same isOutgoing")
                            else:
                                print("is parent")
                                break
                        # check if the text is equal
                        words = current_test['text'].split(" ")
                        for word in words:
                            if word not in message['taggedText']:
                                break
                        print("same text: ", message['taggedText'])
                        if utils_funcs.time_in_range(message['timeReceived'], 2) == True:
                            print("same time")
                            return True
        return False

    '''
    
    '''
    def check_parent_logs(self, parent_name, stdout_reader, stdout_queue):
        time.sleep(20)
        print("after")
        parent_logs = ""
        while not stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = str(stdout_queue.get())
            print("**",str(line))
            if '"messages":' in str(line):
                parent_logs = "{"
                while not ": }" in str(line):
                    if "taggedText" in line:
                        line = str(line).split("HttpKeepersLogger: ")[1].split("\\r\\n'")[0].strip()
                        parent_logs = parent_logs + str(line).replace('\\"','').replace('\\','')
                    else:
                        parent_logs = parent_logs + str(line).split("HttpKeepersLogger: ")[1].split("\\r\\n'")[0].strip()
                    line = str(stdout_queue.get())
                parent_logs = parent_logs + "}"
            if parent_logs == "":
                continue

            specific_log = parent_logs.replace("false", "False").replace("true", "True")
            logs_dict = ast.literal_eval(specific_log)
            print("logs_dict: ", logs_dict)
            log_exist = self.check_messaging_logs(logs_dict, parent_name, True)
            if log_exist == True:
                driver.global_tests_result.append(['True', logs_dict])
                return True
        driver.global_tests_result.append(['False', "No logs received"])
        print("False in parent")
        return False


    def check_child_logs(self, parent_name):
        global logs
        for log in logs:
            specific_log = log.replace("false", "False").replace("true", "True")
            specific_log = specific_log.split("HttpKeepersLogger: ")[1]
            specific_log = specific_log.split("\\r\\n")[0]
            logs_dict = ast.literal_eval(specific_log)
            log_exist = self.check_messaging_logs(logs_dict, parent_name)
            if log_exist == True:
                driver.global_tests_result.append(['True', logs_dict])
                return
        driver.global_tests_result.append(['False', "No logs received"])
        print("False in child side")

    def check_remove_group_logs(self, child_stdout_reader, child_stdout_queue):
        global logs
        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'broadcast', '-a',
                        'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])
        time.sleep(20)
        while not child_stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = child_stdout_queue.get()
            print("line removal: ", line)
            if "eventType" in str(line):
                logs.append(str(line))

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

    def get_keepers_logs(self, s_network, from_child=False):
        global logs
        father_stdout_reader, father_stdout_queue = self.start_listen_to_logs(driver.father_device)
        child_stdout_reader, child_stdout_queue = self.start_listen_to_logs(driver.child_device)

        self.child_open_chat_screen(s_network, from_child)  # child reed the message
        time.sleep(3)
        # uplaod the keepers logs
        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'broadcast', '-a',
                        'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])
        time.sleep(10)
        while not child_stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = child_stdout_queue.get()
            print(line)
            if "taggedText" in str(line):
                logs.append(str(line))

        self.check_child_logs(s_network[sl.PARENT_NAME])
        parent_logs = self.check_parent_logs(s_network[sl.PARENT_NAME], father_stdout_reader, father_stdout_queue)
        if parent_logs == strtobool(driver.current_test[sl.OFFENSIVE]):
            driver.global_tests_result.append(['True', "Logs were received respectively"])
        else:
            driver.global_tests_result.append(['False', "Logs were not received respectively"])

    def return_coordinates_by_resource_id(self, step, parent_name):
        process = subprocess.Popen(['adb','-s', driver.child_device ,'exec-out', 'uiautomator', 'dump', '/dev/tty'],stdout=subprocess.PIPE)  # dump the uiautomator file
        content = str(process.stdout.read())
        splitted_content = re.split("<node", content)
        for node in splitted_content:
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
                    print(str(driver.current_test[sl.MESSAGING_CONTENT]))
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text', '"' +str(driver.current_test[sl.MESSAGING_CONTENT]) +'"'])
                elif step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT and from_child == False:
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'keyevent', '111'])
                    return
                else:
                    print("parenttttt")
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text', s_network[sl.PARENT_NAME][:-1]])
            elif step[sl.ACTION_STEP] == sl.ACTION_CLICK:
                coordinates = self.return_coordinates_by_resource_id(step, s_network[sl.PARENT_NAME])
                subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'tap', coordinates[1] , coordinates[2]])
            time.sleep(3)

    def start_listen_to_logs(self,device):
        # get keepers logcats to a PIPE
        process = subprocess.Popen(['adb', '-s', device, 'logcat', '-s', 'HttpKeepersLogger'],
                                   stdout=subprocess.PIPE)
        stdout_queue = Queue()
        stdout_reader = read_messaging_logs.AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.start()

        return stdout_reader,stdout_queue


    def send_message(self, from_child = False):
        networks = xml_parsing.tests_xml_to_dictionary(sl.APPS_FILE)
        for network in networks:
            if network[sl.APP_NAME] == driver.current_test[sl.TEST_APP_NAME]:
                if driver.current_test[sl.TEST_SIDE] == sl.TEST_RECIVE_SIDE:
                    driver.current_test[sl.CHAT_NAME] = network[sl.CHILD_NAME]
                else:
                    driver.current_test[sl.CHAT_NAME] = network[sl.PARENT_NAME]
                if from_child == False: # send a message to the child
                    driver.connect_driver(network[sl.APP_PACKAGE],network[sl.APP_ACTIVITY])# connect the driver
                    for step in network[sl.STEPS]:
                        driver.global_tests_result.append(components_operations.component_operation(step))
                time.sleep(3)
                self.get_keepers_logs(network, from_child)


    def remove_from_group(self):
        networks = xml_parsing.tests_xml_to_dictionary(sl.APPS_FILE)

        child_stdout_reader, child_stdout_queue = self.start_listen_to_logs(driver.child_device)

        for network in networks:
            if network[sl.APP_NAME] == driver.current_test[sl.TEST_APP_NAME]:
                driver.current_test[sl.CHAT_NAME] = network[sl.GROUP_NAME]
                driver.current_test[sl.CHILD_NAME] = network[sl.CHILD_NAME]
                network[sl.PARENT_NAME] = network[sl.GROUP_NAME]
                driver.connect_driver(network[sl.APP_PACKAGE], network[sl.APP_ACTIVITY])  # connect the driver
                for step in network[sl.STEPS]:
                    if step[sl.CONTENT_STEP] == 'text':
                        print("break")
                        break
                    driver.global_tests_result.append(components_operations.component_operation(step))
                for step in network[sl.REMOVAL_STEPS]:
                    driver.global_tests_result.append(components_operations.component_operation(step))

                self.child_open_chat_screen(network, False)
                break
        self.check_remove_group_logs(child_stdout_reader, child_stdout_queue)


    def test_manage_message(self):
        if driver.current_test[sl.TEST_NAME] == sl.REMOVAL_TEST:  # removal from group test
            self.remove_from_group()
        elif driver.current_test[sl.TEST_SIDE] == sl.TEST_RECIVE_SIDE:
            self.send_message()
        elif driver.current_test[sl.TEST_SIDE] == sl.TEST_SEND_SIDE:
            self.send_message(True)


