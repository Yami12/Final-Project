import unittest
import driver
import xml_parsing
from button_operations import buttonOperations
from input_operations import inpoutOperations
from time import sleep
import html_page
tests_results=[]
flowes = []

class MainTester(unittest.TestCase):

    def run_specific_flow(flow_name):
        flowes = xml_parsing.xml_to_dictionary("xml_file.xml")
        for flow in flowes:
            print(flow['name'],'#',flow_name)
            if flow['name'] == flow_name:
                for test in flow['tests']:
                    driver.current_test = test
                    # if driver.global_driver.current_activity != test['appActivity']:
                    #     driver.global_driver.start_activity("com.keepers", test['appActivity'])#app package, app activity
                    if test['type'] == 'Button' or test['type'] == 'CheckBox':
                        sleep(5)
                        suite = unittest.TestLoader().loadTestsFromTestCase(buttonOperations)
                        result = unittest.TextTestRunner(verbosity=1).run(suite)
                        tests_results.append([flow['name'], test['name'], result])  # save the test result
                    elif test['type'] == 'Entry':
                        suite = unittest.TestLoader().loadTestsFromTestCase(inpoutOperations)
                        result = unittest.TextTestRunner(verbosity=1).run(suite)
                        tests_results.append([flow['name'], test['name'], result])

    def testscaller(self):
        # driver.initialize('Android', '8.0.0', 'My HUAWEI', 'com.keepers',
        #                                                     'com.keeper.common.splash.SplashActivity', '4723', 'Keepers Child Safety.apk')
        # suite = unittest.TestLoader().loadTestsFromTestCase(DownloadApp)
        # result = unittest.TextTestRunner(verbosity=1).run(suite)
        # driver.close_driver()

        # driver.initialize('Android', '7.0', 'Galaxy S6 edge', 'com.keepers', 'com.keeper.common.splash.SplashActivity',
        #                   '4723')
        #parse the xml file of al the tests

        MainTester.run_specific_flow("child's age - above 16")
        html_page.create(tests_results)




# ---START OF SCRIPT
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MainTester)
    result = unittest.TextTestRunner(verbosity=1).run(suite)

