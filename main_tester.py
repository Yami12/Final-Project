'''
This file handles the running of the tests
there is 2 attributes:
tests_results: list of all the tests results
flowes: list of all the flowes
'''

import unittest
import driver
import xml_parsing
from button_operations import buttonOperations
from input_operations import inpoutOperations
import messaging
from time import sleep

tests_results=[]
flowes = []
messaging_functions = {'whatsapp':'whatsapp_message'}
class MainTester(unittest.TestCase):


    def recive_offensive_whatsapp_message(test):
        print("yay 1")

        # suite = unittest.TestLoader().loadTestsFromTestCase(messaging.FatherSentWhatsappMessage)
        # result = unittest.TextTestRunner(verbosity=1).run(suite)
        # tests_results.append("test: {} result: {}".format(test['name'],
        #                                                            result))  # save the test result
        #
        # suite = unittest.TestLoader().loadTestsFromTestCase(messaging.ChildReadWhatsappMessage)
        # result = unittest.TextTestRunner(verbosity=1).run(suite)
        # tests_results.append("test: {} result: {}".format(test['name'],
        #                                                   result))  # save the test result

        suite = unittest.TestLoader().loadTestsFromTestCase(messaging.CheckChildLogs)
        result = unittest.TextTestRunner(verbosity=1).run(suite)


    def run_behvior_test(flow,test):
        driver.initialize_father()
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
                driver.current_test = test
                MainTester.recive_offensive_whatsapp_message(test)
