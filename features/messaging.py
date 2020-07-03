import unittest
import datetime
import time
import ast
from distutils.util import strtobool
import subprocess
from queue import Queue
import re
import sys
from utils import utils_funcs
from utils import driver
from utils import read_messaging_logs
from utils import xml_parsing
from utils import string_list as sl
from components import components_operations

logs = []


class Messaging (unittest.TestCase):

    # def shortDescription(self):
    #     return None

    '''
           function: check_messaging_logs
           description: A function that checks whether the message sent in a test match the received logs
    '''
    def check_messaging_logs(self, logs_dict, chat_name, isParent = False):
        current_test = driver.current_test
        if logs_dict['applicationName'] == current_test['application']:
            if logs_dict['isGroup'] == strtobool(current_test['isGroup']):
                if logs_dict['title'] == chat_name:
                    if isParent:
                        words = current_test['text'].split(" ")
                        for word in words:
                            if word not in logs_dict['quote']:
                                break
                        message = logs_dict
                    else:
                        messages = logs_dict['messages']
                        for message in messages:
                            if (message['isOutgoing'] == True and current_test['side'] == 'send') or (
                                message['isOutgoing'] == False and current_test['side'] == 'recive'):
                                words = current_test['text'].split(" ")
                                for word in words:
                                    if word not in message['taggedText']:
                                        break
                            else:
                                break
                    if utils_funcs.time_in_range(message['timeReceived'], 2) == True:
                        print("\cf1 \\b The found log is: \\b0", logs_dict,"\line")
                        sys.stdout.flush()
                        return True
        return False


    '''
            function: check_parent_logs
            description: A function that checks if logs are received in parent device
    '''
    def check_parent_logs(self, parent_name, stdout_reader, stdout_queue):
        print("\cf1 start to read parent logs...\line")
        sys.stdout.flush()
        time.sleep(30)
        parent_logs = ""

        while not stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = str(stdout_queue.get())
            if '"quote":' in line:
                parent_logs = "{"
                while not "}" in line:
                    if "quote" in line:
                        line = line.split("HttpKeepersLogger: ")[1].split("\\r\\n'")[0].strip()
                        parent_logs = parent_logs + line.replace('\\"','').replace('\\','')
                    else:
                        parent_logs = parent_logs + line.split("HttpKeepersLogger: ")[1].split("\\r\\n'")[0].strip()
                    line = str(stdout_queue.get())

                parent_logs = parent_logs + "}"

            if parent_logs == "":
                continue

            specific_log = parent_logs.replace("false", "False").replace("true", "True")
            logs_dict = ast.literal_eval(specific_log)

            log_exist = self.check_messaging_logs(logs_dict, parent_name, True)
            if log_exist == True:
                driver.global_tests_result[-1]['results'].append(['Passed', logs_dict])
                return True

        driver.global_tests_result[-1]['results'].append(['Failed', "No logs received"])
        print("\cf2 No logs received in parent side \line")
        sys.stdout.flush()
        return False


    '''
            function: check_child_logs
            description: A function that checks if logs are received in child device
    '''
    def check_child_logs(self, parent_name):
        global logs

        for log in logs:
            specific_log = log.replace("false", "False").replace("true", "True")
            specific_log = specific_log.split("HttpKeepersLogger: ")[1]
            specific_log = specific_log.split("\\r\\n")[0]
            logs_dict = ast.literal_eval(specific_log)
            log_exist = self.check_messaging_logs(logs_dict, parent_name)
            if log_exist == True:
                driver.global_tests_result[-1]['results'].append(['Passed', logs_dict])
                return True

        driver.global_tests_result[-1]['results'].append(['Faild', "No logs received"])
        print("\cf2 No logs received in child side \line")
        sys.stdout.flush()
        return False


    '''
            function: check_removal_from_group_logs
            description: A function that checks if the logs that received in child device match the removal details
    '''
    def check_removal_from_group_logs(self, child_stdout_reader, child_stdout_queue):
        global logs
        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'broadcast', '-a',
                        'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS']) # uplaod the keepers logs
        time.sleep(20)
        print("\cf1 start to read child logs... \line")
        sys.stdout.flush()
        while not child_stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = child_stdout_queue.get()
            print("\cf1 line removal: ", line, "\line")
            sys.stdout.flush()
            if "eventType" in str(line):
                logs.append(str(line))
        sys.stdout.flush()
        current_test = driver.current_test

        for log in logs:
            specific_log = log.replace("false", "False").replace("true", "True")
            specific_log = specific_log.split("HttpKeepersLogger: ")[1]
            specific_log = specific_log.split("\\r\\n")[0]
            logs_dict = ast.literal_eval(specific_log)
            if logs_dict['eventData'] == current_test[sl.CHAT_NAME] and "CHILD_REMOVED_FROM" in logs_dict['eventType']:
                driver.global_tests_result[-1]['results'].append(['Passed', logs_dict])
                print("\cf1 \\b The found log is \\b0 : ", logs_dict, "\line")
                sys.stdout.flush()
                print('\cf3 SUCCESS, Removal from group Logs were received respectively \line')
                sys.stdout.flush()
                return True

        driver.global_tests_result[-1]['results'].append(['Failed', "No matching logs"])
        print('\cf2 No matching Removal from group logs \line')
        sys.stdout.flush()
        return False


    '''
            function: get_keepers_logs
            description: A function that gets the keepers logs from the device
    '''
    def get_keepers_logs(self, s_network, from_child=False):
        global logs

        print("\cf1 begin to listen to parent logs... \line")
        sys.stdout.flush()
        father_stdout_reader, father_stdout_queue = self.start_listen_to_logs(driver.father_device)
        print("\cf1 begin to listen to child logs... \line")
        sys.stdout.flush()
        child_stdout_reader, child_stdout_queue = self.start_listen_to_logs(driver.child_device)

        self.child_open_chat_screen(s_network, from_child)  # child reed the message
        time.sleep(3)
        sys.stdout.flush()
        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'broadcast', '-a',
                        'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS']) # uplaod the keepers logs
        time.sleep(10)
        print("\cf1 starting to read child logs... \line")
        sys.stdout.flush()
        while not child_stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = child_stdout_queue.get()
            if "taggedText" in str(line):
                logs.append(str(line))

        print("\cf1 checking child logs. \line")
        sys.stdout.flush()
        child_logs = self.check_child_logs(s_network[sl.PARENT_NAME])
        if child_logs:
            print("{\cf3 SUCCESS, Child's Logs were received respectively \line}")
            sys.stdout.flush()
            driver.global_tests_result[-1]['results'].append(['Passed', "Child's Logs were received respectively"])
        else:
            print("\cf2 FAILED, Child's Logs were not received respectively \line")
            sys.stdout.flush()
            driver.global_tests_result[-1]['results'].append(['Failed', "Child's Logs were not received respectively"])
            return False
        print("\cf1 checking parent logs. \line")
        parent_logs = self.check_parent_logs(s_network[sl.PARENT_NAME], father_stdout_reader, father_stdout_queue)
        if parent_logs == strtobool(driver.current_test[sl.OFFENSIVE]):
            print("\cf3 SUCCESS, Parent's Logs were received respectively \line")
            sys.stdout.flush()
            driver.global_tests_result[-1]['results'].append(['Passed', "Logs were received respectively"])
            return True

        print("\cf2 FAILED, Parent's Logs were not received respectively \line")
        sys.stdout.flush()
        driver.global_tests_result[-1]['results'].append(['Failed', "Logs were not received respectively"])
        return False


    '''
            function: get_coordinates_by_resource_id
            description: A function that returns a device component coordinates by its resource id
    '''
    def get_coordinates_by_resource_id(self, step, parent_name):
        print("\cf1 searching for coordinates \line")
        sys.stdout.flush()
        process = subprocess.Popen(['adb','-s', driver.child_device ,'exec-out', 'uiautomator', 'dump', '/dev/tty'],stdout=subprocess.PIPE)  # dump the uiautomator file
        content = str(process.stdout.read())
        splitted_content = re.split("<node", content)

        for node in splitted_content:
            if step[sl.TYPE_STEP] == sl.TYPE_ID and step[sl.ID_STEP] in node: # id
                process.kill()
                break
            elif step[sl.TYPE_STEP] == sl.TYPE_UIAUTOMATOR and 'class="android.widget.ImageView"' not in node: # uiautomator
                if step[sl.CONTENT_STEP] == sl.CHAT_NAME:
                    if parent_name in node:
                        process.kill()
                        break
                elif 'content-desc="' + step[sl.CONTENT_STEP] in node:
                    process.kill()
                    break
            elif step[sl.TYPE_STEP] == sl.TYPE_CLASS and 'class="' + step[sl.ID_STEP] in node: # class
                process.kill()
                break

        bounds = re.search('bounds="\[([0-9]+),([0-9]+)\]', node)
        if not bounds:
            print("\cf2 bounds not fond. \line")
            sys.stdout.flush()
        else:
            print("\cf1 \\b bounds fond:\\b0 ", bounds, "\line")
            sys.stdout.flush()
        return bounds


    '''
           function: child_open_chat_screen
           description: A function that open the app chat screen in the child device
    '''
    def child_open_chat_screen(self, s_network, from_child):

        print("\cf1 connecting to child device... \line")
        sys.stdout.flush()
        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'start', '-n', s_network[sl.APP_PACKAGE]+"/" + s_network[sl.APP_ACTIVITY]]) # launch the application
        time.sleep(3)
        print("\cf1 running the opening steps \line")
        sys.stdout.flush()
        for step in s_network[sl.STEPS]:
            if step[sl.ACTION_STEP] == sl.ACTION_SEND_KEYS: # send keys action
                if step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT and from_child == True:
                    driver.sending_time = datetime.datetime.now()  # save the sending time
                    print('\cf1 enter text. run command: adb -s ' + driver.child_device +' shell input text: "' +str(
                        driver.current_test[sl.MESSAGING_CONTENT]) + '"\line')
                    sys.stdout.flush()
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text', '"' +str(driver.current_test[sl.MESSAGING_CONTENT]) +'"'])
                elif step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT and from_child == False:
                    print('\cf1 hide keyboard. run command: adb -s ' + driver.child_device + ' shell input keyevent 111 \line')
                    sys.stdout.flush()
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'keyevent', '111'])
                    return
                else:
                    print('\cf1 enter text. run command: adb -s ' + driver.child_device + ' shell input text : "' + s_network[sl.PARENT_NAME][:-1] + '"\line')
                    sys.stdout.flush()
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text', s_network[sl.PARENT_NAME][:-1]])
            elif step[sl.ACTION_STEP] == sl.ACTION_CLICK: # click action
                coordinates = self.get_coordinates_by_resource_id(step, s_network[sl.PARENT_NAME])
                print('\cf1 click. run command: adb -s' + driver.child_device + 'shell input tap ' +str(coordinates[1]) + ' ' + str(coordinates[2]),"\line")
                sys.stdout.flush()
                subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'tap', coordinates[1] , coordinates[2]])
            time.sleep(3)


    '''
           function: start_listen_to_logs
           description: A function that listen to logs that received from the device
    '''
    def start_listen_to_logs(self,device):
        # get keepers logcats to a PIPE
        process = subprocess.Popen(['adb', '-s', device, 'logcat', '-s', 'HttpKeepersLogger'],
                                   stdout=subprocess.PIPE)
        stdout_queue = Queue()
        stdout_reader = read_messaging_logs.AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.start()

        return stdout_reader, stdout_queue


    '''
           function: send_message
           description: A function that send a message to/from the child (according to from_child flag)
    '''
    def send_message(self, from_child = False):
        networks = xml_parsing.tests_xml_to_dictionary(sl.APPS_FILE)
        for network in networks:
            if network[sl.APP_NAME] == driver.current_test[sl.TEST_APP_NAME]:
                if driver.current_test[sl.TEST_SIDE] == sl.TEST_RECIVE_SIDE:
                    driver.current_test[sl.CHAT_NAME] = network[sl.CHILD_NAME]
                else:
                    driver.current_test[sl.CHAT_NAME] = network[sl.PARENT_NAME]
                if from_child == False: # send a message to the child
                    print("\cf1 connecting to appium server... \line")
                    sys.stdout.flush()
                    driver.connect_driver(network[sl.APP_PACKAGE],network[sl.APP_ACTIVITY])# connectind the driver
                    print("\cf1 starting to run the test steps \line")
                    sys.stdout.flush()
                    for step in network[sl.STEPS]:
                        driver.global_tests_result[-1]['results'].append(components_operations.component_operation(step))
                time.sleep(3)
                print("\cf1 getting keepers logs from child and parent devices \line")
                sys.stdout.flush()
                return self.get_keepers_logs(network, from_child)


    '''
           function: remove_from_group
           description: A function that removes the child from an app group
    '''
    def remove_from_group(self):
        networks = xml_parsing.tests_xml_to_dictionary(sl.APPS_FILE)

        child_stdout_reader, child_stdout_queue = self.start_listen_to_logs(driver.child_device)

        for network in networks:
            if network[sl.APP_NAME] == driver.current_test[sl.TEST_APP_NAME]:
                driver.current_test[sl.CHAT_NAME] = network[sl.GROUP_NAME]
                driver.current_test[sl.CHILD_NAME] = network[sl.CHILD_NAME]
                network[sl.PARENT_NAME] = network[sl.GROUP_NAME]

                print("\cf1 removing the child from group: ", network[sl.GROUP_NAME], "\line")
                sys.stdout.flush()
                driver.connect_driver(network[sl.APP_PACKAGE], network[sl.APP_ACTIVITY])  # connect the driver

                print("\cf1 starting to run the test steps \line")
                sys.stdout.flush()
                for step in network[sl.STEPS]:
                    if step[sl.CONTENT_STEP] == 'text':
                        break
                    driver.global_tests_result[-1]['results'].append(components_operations.component_operation(step))
                for step in network[sl.REMOVAL_STEPS]:
                    driver.global_tests_result[-1]['results'].append(components_operations.component_operation(step))

                print("\cf1 open the chat screen in child device \line")
                sys.stdout.flush()
                self.child_open_chat_screen(network, False)
                break

        print("\cf1 getting keepers logs from child device \line")
        sys.stdout.flush()
        self.check_removal_from_group_logs(child_stdout_reader, child_stdout_queue)


    '''
           function: test_run
           description: A function that runs the current test
    '''
    def test_run(self):
        if driver.current_test[sl.TEST_NAME] == sl.REMOVAL_TEST:
            driver.test_result = self.remove_from_group()
        elif driver.current_test[sl.TEST_SIDE] == sl.TEST_RECIVE_SIDE: # child recive a message
            print("\cf1 sending a message to the child... \line")
            sys.stdout.flush()
            driver.test_result = self.send_message()
        elif driver.current_test[sl.TEST_SIDE] == sl.TEST_SEND_SIDE: # child send a message
            print("\cf1 sending a message from the child... \line")
            sys.stdout.flush()
            driver.test_result = self.send_message(True)


