"""
The file handles messaging and removal from group tests
"""
import unittest
import datetime
import time
import ast
from distutils.util import strtobool
import subprocess
from queue import Queue

from utils import driver
from utils import read_messaging_logs
from utils import xml_parsing
from utils import string_list as sl
from utils import utils_funcs as uf

from components import components_operations

logs = []


class Messaging (unittest.TestCase):

    '''
           function: check_messaging_logs
           description: A function that checks whether the message that been sent/received in the test match the received logs
    '''
    def check_messaging_logs(self, logs_dict, chat_name, isParent = False):
        current_test = driver.current_test
        if logs_dict['applicationName'] == current_test['application']:
            if logs_dict['isGroup'] == strtobool(current_test['isGroup']):
                if logs_dict['title'] == chat_name:
                    if isParent: # log in parent side
                        words = current_test['text'].split(" ")
                        for word in words:
                            if word not in logs_dict['quote']:
                                break
                        message = logs_dict
                    else: # log in child side
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
                    if uf.time_in_range(message['timeReceived'], 2) == True:
                        uf.print_log("\cf1 \\b The found log is: \\b0" + logs_dict + "\line")
                        return True
        return False


    '''
            function: check_parent_logs
            description: A function that checks if logs are received in parent device
    '''
    def check_parent_logs(self, parent_name, stdout_reader, stdout_queue):
        uf.print_log("\cf1 start to read parent logs...\line")
        time.sleep(30)
        parent_logs = ""

        while not stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = str(stdout_queue.get())
            if '"quote":' in line: # the beginning of the log
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

            # convert the log string to dictionary
            specific_log = parent_logs.replace("false", "False").replace("true", "True")
            logs_dict = ast.literal_eval(specific_log)

            log_exist = self.check_messaging_logs(logs_dict, parent_name, True)
            if log_exist == True:
                driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_PASSED, logs_dict])
                return True

        driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_FAILED, "No logs received"])
        uf.print_log("\cf2 No logs received in parent side \line")
        return False


    '''
            function: check_child_logs
            description: A function that checks if logs are received in child device
    '''
    def check_child_logs(self, parent_name):
        global logs

        for log in logs:
            # convert the log string to dictionary
            specific_log = log.replace("false", "False").replace("true", "True")
            specific_log = specific_log.split("HttpKeepersLogger: ")[1]
            specific_log = specific_log.split("\\r\\n")[0]
            logs_dict = ast.literal_eval(specific_log)
            log_exist = self.check_messaging_logs(logs_dict, parent_name)
            if log_exist == True:
                driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_PASSED, logs_dict])
                return True

        driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_FAILED, "No logs received"])
        uf.print_log("\cf2 No logs received in child side \line")
        return False


    '''
            function: check_removal_from_group_logs
            description: A function that checks if the logs that send from the child device match the removal details
    '''
    def check_removal_from_group_logs(self, child_stdout_reader, child_stdout_queue):
        global logs
        process = subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'broadcast', '-a',
                        'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS']) # uplaod the keepers logs
        time.sleep(20)
        uf.print_log("\cf1 start to read child logs... \line")
        while not child_stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = str(child_stdout_queue.get())
            if "eventType" in line:
                logs.append(line)

        current_test = driver.current_test

        for log in logs:
            # convert the log string to dictionary
            specific_log = log.replace("false", "False").replace("true", "True")
            specific_log = specific_log.split("HttpKeepersLogger: ")[1]
            specific_log = specific_log.split("\\r\\n")[0]
            logs_dict = ast.literal_eval(specific_log)
            if logs_dict['eventData'] == current_test[sl.CHAT_NAME] and "CHILD_REMOVED_FROM" in logs_dict['eventType']:
                driver.global_tests_result[-1]['results'].append(['Passed', logs_dict])
                uf.print_log("\cf1 \\b The found log is \\b0 : " + logs_dict + "\line \cf3 SUCCESS, Removal from group Logs were received respectively \line")
                return True

        driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_FAILED, "No matching logs"])
        uf.print_log("\cf2 No matching Removal from group logs \line")
        process.kill
        return False


    '''
            function: get_keepers_logs
            description: A function that gets the keepers logs from the device
    '''
    def get_keepers_logs(self, s_network, from_child=False):
        global logs

        uf.print_log("\cf1 begin to listen to parent logs... \line")
        father_proc, father_stdout_reader, father_stdout_queue = self.start_listen_to_logs(driver.father_device)

        uf.print_log("\cf1 begin to listen to child logs... \line")
        child_proc, child_stdout_reader, child_stdout_queue = self.start_listen_to_logs(driver.child_device)

        self.child_open_chat_screen(s_network, from_child)  # child reed the message
        time.sleep(3)

        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'broadcast', '-a',
                        'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])# uplaod the keepers logs
        time.sleep(10)
        uf.print_log("\cf1 starting to read child logs... \line")
        while not child_stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = child_stdout_queue.get()
            if "taggedText" in str(line):
                logs.append(str(line))

        uf.print_log("\cf1 checking child logs. \line")
        child_logs = self.check_child_logs(s_network[sl.PARENT_NAME])
        if child_logs: # child's Logs were received respectively
            uf.print_log("\cf3 SUCCESS, Child's Logs were received respectively \line")
            driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_PASSED, "Child's Logs were received respectively"])
        else:
            uf.print_log("\cf2 FAILED, Child's Logs were not received respectively \line")
            driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_FAILED, "Child's Logs were not received respectively"])
            return False

        uf.print_log("\cf1 checking parent logs. \line")
        parent_logs = self.check_parent_logs(s_network[sl.PARENT_NAME], father_stdout_reader, father_stdout_queue)
        if parent_logs == strtobool(driver.current_test[sl.OFFENSIVE]):# parent's Logs were received respectively
            uf.print_log("\cf3 SUCCESS, Parent's Logs were received respectively \line")
            driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_PASSED, "Logs were received respectively"])
            return True

        uf.print_log("\cf2 FAILED, Parent's Logs were not received respectively \line")
        driver.global_tests_result[-1][sl.TEST_RESULTS].append([sl.TEST_FAILED, "Logs were not received respectively"])
        father_proc.kill()
        child_proc.kill()
        return False

    '''
           function: child_open_chat_screen
           description: A function that open the app chat screen in the child device
    '''
    def child_open_chat_screen(self, s_network, from_child):

        uf.print_log("\cf1 connecting to child device... \line")
        proc = subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'start', '-n', s_network[sl.APP_PACKAGE]+"/" + s_network[sl.APP_ACTIVITY]]) # launch the application
        time.sleep(3)
        uf.print_log("\cf1 running the opening steps \line")
        for step in s_network[sl.STEPS]:
            if step[sl.ACTION_STEP] == sl.ACTION_SEND_KEYS: # send keys action
                if step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT and from_child == True:
                    driver.sending_time = datetime.datetime.now()  # save the sending time
                    uf.print_log('\cf1 enter text. run command: adb -s ' + driver.child_device +' shell input text: "' +str(
                        driver.current_test[sl.MESSAGING_CONTENT]) + '"\line')
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text', '"' +str(driver.current_test[sl.MESSAGING_CONTENT]) +'"'])
                elif step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT and from_child == False:
                    uf.print_log('\cf1 hide keyboard. run command: adb -s ' + driver.child_device + ' shell input keyevent 111 \line')
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'keyevent', '111'])
                    return
                else:
                    uf.print_log('\cf1 enter text. run command: adb -s ' + driver.child_device + ' shell input text : "' + s_network[sl.PARENT_NAME][:-1] + '"\line')
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text', s_network[sl.PARENT_NAME][:-1]])
            elif step[sl.ACTION_STEP] == sl.ACTION_CLICK: # click action
                coordinates = uf.get_coordinates_by_resource_id(step, s_network[sl.PARENT_NAME])
                uf.print_log("\cf1 click. run command: adb -s" + driver.child_device + "shell input tap " +str(coordinates[1]) + " " + str(coordinates[2]) + "\line")
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

        return process, stdout_reader, stdout_queue


    '''
           function: send_message
           description: A function that send a message to/from the child (according to from_child flag)
    '''
    def send_message(self, from_child = False):
        networks = xml_parsing.tests_xml_to_dictionary(sl.APPS_FILE) # get the list of all the networks
        for network in networks:
            if network[sl.APP_NAME] == driver.current_test[sl.TEST_APP_NAME]:
                if driver.current_test[sl.TEST_SIDE] == sl.TEST_RECIVE_SIDE: # child receives a message
                    driver.current_test[sl.CHAT_NAME] = network[sl.CHILD_NAME]
                else: # child sends a message
                    driver.current_test[sl.CHAT_NAME] = network[sl.PARENT_NAME]
                if from_child == False: # send a message to the child
                    uf.print_log("\cf1 connecting to appium server... \line")
                    driver.connect_driver(network[sl.APP_PACKAGE],network[sl.APP_ACTIVITY])# connectind the driver
                    uf.print_log("\cf1 starting to run the test steps \line")
                    for step in network[sl.STEPS]:
                        driver.global_tests_result[-1]['results'].append(components_operations.component_operation(step))
                time.sleep(3)

                uf.print_log("\cf1 getting keepers logs from child and parent devices \line")
                return self.get_keepers_logs(network, from_child)


    '''
           function: remove_from_group
           description: A function that removes the child from an app group
    '''
    def remove_from_group(self):
        networks = xml_parsing.tests_xml_to_dictionary(sl.APPS_FILE) # get list of all the networks

        process, child_stdout_reader, child_stdout_queue = self.start_listen_to_logs(driver.child_device)
        uf.print_log("\cf1 begin to listen to child logs... \line")
        for network in networks:
            if network[sl.APP_NAME] == driver.current_test[sl.TEST_APP_NAME]:
                driver.current_test[sl.CHAT_NAME] = network[sl.GROUP_NAME]
                driver.current_test[sl.CHILD_NAME] = network[sl.CHILD_NAME]
                network[sl.PARENT_NAME] = network[sl.GROUP_NAME]

                uf.print_log("\cf1 removing the child from group: " + network[sl.GROUP_NAME] + "\line connecting to appium server...")
                driver.connect_driver(network[sl.APP_PACKAGE], network[sl.APP_ACTIVITY])  # connect the driver

                uf.print_log("\cf1 starting to run the test steps \line")
                for step in network[sl.STEPS]:
                    if step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT:
                        break
                    driver.global_tests_result[-1][sl.TEST_RESULTS].append(components_operations.component_operation(step))
                for step in network[sl.REMOVAL_STEPS]: # removal steps
                    driver.global_tests_result[-1][sl.TEST_RESULTS].append(components_operations.component_operation(step))

                uf.print_log("\cf1 open the chat screen in child device \line")
                self.child_open_chat_screen(network, False)
                break

        uf.print_log("\cf1 getting keepers logs from child device \line")
        process.kill()
        return self.check_removal_from_group_logs(child_stdout_reader, child_stdout_queue)



    '''
           function: test_run
           description: A function that runs the current test
    '''
    def test_run(self):
        if driver.current_test[sl.TEST_NAME] == sl.REMOVAL_TEST: # removal from group test
            driver.test_result = self.remove_from_group()
        elif driver.current_test[sl.TEST_SIDE] == sl.TEST_RECIVE_SIDE: # child receive a message
            uf.print_log("\cf1 sending a message to the child... \line")
            driver.test_result = self.send_message()
        elif driver.current_test[sl.TEST_SIDE] == sl.TEST_SEND_SIDE: # child send a message
            uf.print_log("\cf1 sending a message from the child... \line")
            driver.test_result = self.send_message(True)

