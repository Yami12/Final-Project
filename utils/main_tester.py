'''
This file handles the running of the tests
there is 2 attributes:
tests_results: list of all the tests results
flowes: list of all the flowes
'''

import unittest
import os

from utils import driver
from utils import xml_parsing
from utils import string_list as sl
import time
from features import messaging

from components import components_tests


tests_results = []
flowes = []
messaging_functions = {'whatsapp':'whatsapp_message'}
class MainTester(unittest.TestCase):

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

    '''
        function:run_specific_flow
        description: run the given flow on the android phone
        parameters:
        flow_name - the name of the flow to run
    '''
    def run_specific_behvior_flow(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(components_tests.ComponentsTest)
        result = unittest.TextTestRunner(verbosity=1).run(suite)


    def run_messaging_feature_test(self, test_name, s_network_name):
        tests = xml_parsing.feature_xml_to_dictionary(sl.MESSAGING_FEATURE_FILE)# converts the xml file to list of diction
        for test in tests:
            if test['name'] == test_name or test_name == sl.ALL:
                test[sl.TEST_APP_NAME] = s_network_name
                driver.current_test = test
                # driver.current_s_network = s_network_name

                suite = unittest.TestLoader().loadTestsFromTestCase(messaging.Messaging)
                result = unittest.TextTestRunner(verbosity=1).run(suite)
                tests_results.append("test: {} result: {}".format(test['name'], result))  # save the test result

        return