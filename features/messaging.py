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
            print("same 'app name'")
            if logs_dict['isGroup'] == strtobool(current_test['isGroup']):
                print("same 'is group'")
                if logs_dict['title'] == chat_name:
                    print("same 'title'")
                    messages = logs_dict['messages']
                    for message in messages:
                        if not isParent:
                            if (message['isOutgoing'] == True and current_test['side'] == 'send') or (
                                message['isOutgoing'] == False and current_test['side'] == 'recive'):
                                print("same 'isOutgoing'")
                            else:
                                break
                        # check if the text is equal
                        words = current_test['text'].split(" ")
                        for word in words:
                            if word not in message['taggedText']:
                                break
                        print("same 'text': ", message['taggedText'])
                        if utils_funcs.time_in_range(message['timeReceived'], 2) == True:
                            print("same 'time'")
                            print("The found log is: ", logs_dict)
                            return True
        print("No matching logs")
        return False

    '''
    
    '''
    def check_parent_logs(self, parent_name, stdout_reader, stdout_queue):
        print("start to read parent logs...")
        time.sleep(20)
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
                driver.global_tests_result[-1]['results'].append(['True', logs_dict])
                return True
        driver.global_tests_result[-1]['results'].append(['False', "No logs received"])
        print("No logs received in parent side")
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
                driver.global_tests_result[-1]['results'].append(['True', logs_dict])
                return
        driver.global_tests_result[-1]['results'].append(['False', "No logs received"])
        print("No logs received in child side")

    def check_removal_from_group_logs(self, child_stdout_reader, child_stdout_queue):
        global logs
        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'broadcast', '-a',
                        'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])
        time.sleep(20)
        print("start to read child logs...")
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
                driver.global_tests_result[-1]['results'].append(['True', logs_dict])
                print("The found log is : ", logs_dict)
                return True

        driver.global_tests_result[-1]['results'].append(['False', "No matching logs"])
        print("No matching logs")
        return False

    def get_keepers_logs(self, s_network, from_child=False):
        global logs
        print("begin to listen to parent logs...")
        father_stdout_reader, father_stdout_queue = self.start_listen_to_logs(driver.father_device)
        print("begin to listen to child logs...")
        child_stdout_reader, child_stdout_queue = self.start_listen_to_logs(driver.child_device)

        self.child_open_chat_screen(s_network, from_child)  # child reed the message
        time.sleep(3)
        # uplaod the keepers logs
        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'broadcast', '-a',
                        'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])
        time.sleep(10)
        print("start to read child logs...")
        while not child_stdout_reader.stopped():  # the queue is empty and the thread terminated
            line = child_stdout_queue.get()
            if "taggedText" in str(line):
                logs.append(str(line))
        print("checking child logs.")
        self.check_child_logs(s_network[sl.PARENT_NAME])
        parent_logs = self.check_parent_logs(s_network[sl.PARENT_NAME], father_stdout_reader, father_stdout_queue)
        if parent_logs == strtobool(driver.current_test[sl.OFFENSIVE]):
            print("SUCCESS, Logs were received respectively")
            driver.global_tests_result[-1]['results'].append(['True', "Logs were received respectively"])
        else:
            print("FAILED, Logs were not received respectively")
            driver.global_tests_result[-1]['results'].append(['False', "Logs were not received respectively"])

    def get_coordinates_by_resource_id(self, step, parent_name):
        print("searching for coordinates of ", step[sl.ID_STEP])
        process = subprocess.Popen(['adb','-s', driver.child_device ,'exec-out', 'uiautomator', 'dump', '/dev/tty'],stdout=subprocess.PIPE)  # dump the uiautomator file
        content = str(process.stdout.read())
        splitted_content = re.split("<node", content)
        for node in splitted_content:
            if step[sl.TYPE_STEP] == sl.TYPE_ID and step[sl.ID_STEP] in node: # id
                process.kill()
                break
            elif step[sl.TYPE_STEP] == sl.TYPE_UIAUTOMATOR and 'class="android.widget.ImageView"' not in node:
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
        print("find: ", bounds)
        return bounds




    def child_open_chat_screen(self, s_network, from_child):
        # launch the application
        print("connecting to child device...")
        subprocess.run(['adb', '-s', driver.child_device, 'shell', 'am', 'start', '-n', s_network[sl.APP_PACKAGE]+"/" + s_network[sl.APP_ACTIVITY]])
        time.sleep(3)
        print("steps:")
        for step in s_network[sl.STEPS]:
            if step[sl.ACTION_STEP] == sl.ACTION_SEND_KEYS :
                if step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT and from_child == True:
                    driver.sending_time = datetime.datetime.now()  # save the sending time
                    print('enter text. run command: adb -s' + driver.child_device +'shell input text' +str(
                        driver.current_test[sl.MESSAGING_CONTENT]))
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text', '"' +str(driver.current_test[sl.MESSAGING_CONTENT]) +'"'])
                elif step[sl.CONTENT_STEP] == sl.MESSAGING_CONTENT and from_child == False:
                    print('hide keyboard. run command: adb -s' + driver.child_device + 'shell input keyevent 111')
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'keyevent', '111'])
                    return
                else:
                    print('enter text. run command: adb -s' + driver.child_device + 'shell input text' + s_network[sl.PARENT_NAME][:-1])
                    subprocess.run(['adb', '-s', driver.child_device, 'shell', 'input', 'text', s_network[sl.PARENT_NAME][:-1]])
            elif step[sl.ACTION_STEP] == sl.ACTION_CLICK:
                coordinates = self.get_coordinates_by_resource_id(step, s_network[sl.PARENT_NAME])
                print('click. run command: adb -s' + driver.child_device + 'shell input tap ' +str(coordinates[1]) + ' ' + str(coordinates[2]))
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
                        driver.global_tests_result[-1]['results'].append(components_operations.component_operation(step))
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
                print("removing the child from group: ", network[sl.GROUP_NAME])
                driver.connect_driver(network[sl.APP_PACKAGE], network[sl.APP_ACTIVITY])  # connect the driver
                print("steps:")
                for step in network[sl.STEPS]:
                    if step[sl.CONTENT_STEP] == 'text':
                        break
                    driver.global_tests_result[-1]['results'].append(components_operations.component_operation(step))
                for step in network[sl.REMOVAL_STEPS]:
                    driver.global_tests_result[-1]['results'].append(components_operations.component_operation(step))

                self.child_open_chat_screen(network, False)
                break
        self.check_removal_from_group_logs(child_stdout_reader, child_stdout_queue)


    def test_manage_message(self):
        if driver.current_test[sl.TEST_SIDE] == sl.TEST_RECIVE_SIDE: # child recive a message
            print("sending a message to the child...")
            self.send_message()
        elif driver.current_test[sl.TEST_SIDE] == sl.TEST_SEND_SIDE: # child send a message
            print("sending a message from the child...")
            self.send_message(True)
        else: # child be removed from group
            self.remove_from_group()


