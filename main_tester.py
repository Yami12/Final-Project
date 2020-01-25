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
from time import sleep

tests_results=[]
flowes = []

class MainTester(unittest.TestCase):
    '''
        function:run_specific_flow
        description: run the given flow on the android phone
        parameters:
        flow_name - the name of the flow to run
        '''
    def run_specific_flow(flow_name):
        flowes = xml_parsing.xml_to_dictionary("xml_file.xml")# converts the xml file to list of dictionaries
        #go over all the flowes
        for flow in flowes:
            if flow['name'] == flow_name:# the desired flow
                for test in flow['tests']:
                    driver.current_test = test
                    #TODO check the current app activity:
                    # if driver.global_driver.current_activity != test['appActivity']:
                    #     driver.global_driver.start_activity("com.keepers", test['appActivity'])#app package, app activity

                    #button or checkbox
                    if test['type'] == 'Button' or test['type'] == 'CheckBox':
                        sleep(3)
                        suite = unittest.TestLoader().loadTestsFromTestCase(buttonOperations)
                        result = unittest.TextTestRunner(verbosity=1).run(suite)
                        tests_results.append("flow: {} test: {} result: {}".format(flow['name'], test['name'],
                                                                                   result))  # save the test result
                    #input
                    elif test['type'] == 'Entry':
                        suite = unittest.TestLoader().loadTestsFromTestCase(inpoutOperations)
                        result = unittest.TextTestRunner(verbosity=1).run(suite)
                        tests_results.append("flow: {} test: {} result: {}".format(flow['name'], test['name'], result))# save the test result
