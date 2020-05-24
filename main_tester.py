'''
This file handles the running of the tests
there is 2 attributes:
tests_results: list of all the tests results
flowes: list of all the flowes
'''
import time
from multiprocessing.dummy import Pool as ThreadPool
import unittest
import driver
import xml_parsing
from button_operations import buttonOperations
from input_operations import inpoutOperations
import messaging
from time import sleep
from threading import Thread
import subprocess
from queue import Queue
import re
from read_messaging_logs import AsynchronousFileReader

logs = []
tests_results=[]
flowes = []
messaging_functions = {'whatsapp':'whatsapp_message'}
class MainTester(unittest.TestCase):

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

    def child_read_messages(app_package):

        #get keepers logcats to a PIPE
        process = subprocess.Popen(['adb', '-s', 'emulator-5554', 'logcat', '-s', 'HttpKeepersLogger'],
                                   stdout=subprocess.PIPE)
        stdout_queue = Queue()
        stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.start()

        #launch the application
        subprocess.run(['adb', 'shell', 'am', 'start', '-n', app_package])
        #click the 'search' button
        subprocess.run(['adb', 'shell', 'input', 'keyevent', '84'])
        #write the contact name
        subprocess.run(['adb', 'shell', 'input', 'text', 'Father'])
        #enter the contact conversation
        MainTester.enter_contact_conversation(MainTester)
        time.sleep(15)

        #uplaod the keepers logs
        subprocess.run(['adb', 'shell', 'am', 'broadcast', '-a', 'com.keepers.childmodule.ACTION_UPLOAD_CONVERSATIONS'])
        time.sleep(15)
        #TODO check how to kill thread, how to check thatthe queu is empty and remove the break and replace the while condition
        while(True):
            line = stdout_queue.get()
            if "taggedText" in str(line):
                logs.append(str(line))
                print(logs)
                break


    def recive_offensive_whatsapp_message(test):

        #send whatsapp message to child
        suite = unittest.TestLoader().loadTestsFromTestCase(messaging.FatherSentWhatsappMessage)
        result = unittest.TextTestRunner(verbosity=1).run(suite)
        tests_results.append("test: {} result: {}".format(test['name'], result))  # save the test result

        #child read the message
        MainTester.child_read_messages('com.whatsapp/com.whatsapp.HomeActivity')
        print('exit')

        #check application logs
        suite = unittest.TestLoader().loadTestsFromTestCase(messaging.CheckChildLogs)
        result = unittest.TextTestRunner(verbosity=1).run(suite)


    def run_behvior_test(flow, test):
        driver.initialize_father('com.keepers', 'com.keeper.common.splash.SplashActivity')
        # button or checkbox
        if test['type'] == 'Button' or test['type'] == 'CheckBox':
            sleep(3)
            suite = unittest.TestLoader().loadTestsFromTestCase(buttonOperations)
            result = unittest.TextTestRunner(verbosity=1).run(suite)
            tests_results.append("flow: {} test: {} result: {}".format(flow['name'], test['name'],
                                                                       result))  # save the test result
        # input
        elif test['type'] == 'Entry':
            suite = unittest.TestLoader().loadTestsFromTestCase(inpoutOperations)
            result = unittest.TextTestRunner(verbosity=1).run(suite)
            tests_results.append(
                "flow: {} test: {} result: {}".format(flow['name'], test['name'], result))  # save the test result

    '''
        function:run_specific_flow
        description: run the given flow on the android phone
        parameters:
        flow_name - the name of the flow to run
        '''
    def run_specific_behvior_flow(flow_name):
        flowes = xml_parsing.component_xml_to_dictionary("components_behavior_tests.xml")# converts the xml file to list of dictionaries
        #go over all the flowes
        for flow in flowes:
            if flow['name'] == flow_name:# the desired flow
                for test in flow['tests']:
                    driver.current_test = test
                    if test['appActivity'] != driver.global_driver.current_activity:
                        driver.global_driver.start_activity('com.keepers',test['appActivity'])
                        sleep(10)

                    MainTester.run_test(flow, test)


    def run_specific_behvior_test(flow_name, test_name):
        for flow in flowes:
            if flow['name'] == flow_name:  # the desired flow
                for test in flow['tests']:
                    if test['name'] == test_name:
                        if driver.global_driver.current_activity != test['appActivity']:
                            driver.global_driver.start_activity("com.keepers", test['appActivity'])#app package, app activity
                            MainTester.run_behvior_test(flow, test)


    def run_messaging_feature_test(test_name):
        tests = xml_parsing.feature_xml_to_dictionary("messaging_feature_tests.xml")# converts the xml file to list of diction
        for test in tests:
            if test['name'] == test_name:
                print("yay")
                driver.current_test = test
                MainTester.recive_offensive_whatsapp_message(test)