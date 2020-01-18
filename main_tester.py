import unittest
import driver
from install_child_side import InstallChildSide
from download_app import DownloadApp
import xml_parsing
from button_operations import buttonOperations
from input_operations import inpoutOperations
from time import sleep
tests_results=[]

class MainTester(unittest.TestCase):



    # def setUp(self):
    #     "Setup for the test"
    #     driver.initialize('Android', '8.0.0', 'My HUAWEI', 'com.keepers',
    #                                   'com.keeper.common.splash.SplashActivity', '4723', 'Keepers Child Safety.apk')
    #     # self.desired_caps = {}
    #     # self.desired_caps['platformName'] = 'Android'
    #     # self.desired_caps['platformVersion'] = '8.0.0'
    #     # self.desired_caps['deviceName'] = 'My HUAWEI'
    #     # # Returns abs path relative to this file and not cwd
    #     # self.desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Keepers Child Safety.apk'))
    #     # self.desired_caps['appPackage'] = 'com.keepers'
    #     # self.desired_caps['appActivity'] = 'com.keeper.common.splash.SplashActivity'
    #     # self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)


    def tests_a_caller(self):
        # driver.initialize('Android', '8.0.0', 'My HUAWEI', 'com.keepers',
        #                                                     'com.keeper.common.splash.SplashActivity', '4723', 'Keepers Child Safety.apk')
        # suite = unittest.TestLoader().loadTestsFromTestCase(DownloadApp)
        # result = unittest.TextTestRunner(verbosity=1).run(suite)
        # driver.close_driver()

        driver.initialize('Android', '7.0', 'Galaxy S6 edge', 'com.keepers', 'com.keeper.common.splash.SplashActivity',
                          '4723')
        #parse the xml file
        flowes=xml_parsing.xml_to_dictionary("xml_file.xml")
        for flow in flowes:
            for test in flow['tests']:
                driver.current_test = test
                # if driver.global_driver.current_activity != test['appActivity']:
                #     driver.global_driver.start_activity("com.keepers", test['appActivity'])#app package, app activity
                if test['type'] == 'button':
                    sleep(5)
                    suite = unittest.TestLoader().loadTestsFromTestCase(buttonOperations)
                    result = unittest.TextTestRunner(verbosity=1).run(suite)
                    tests_results.append("flow: {} test: {} result: {}".format(flow['name'],test['name'],result))#save the test result
                elif test['type']== 'input':
                    print("----1----")
                    suite = unittest.TestLoader().loadTestsFromTestCase(inpoutOperations)
                    result = unittest.TextTestRunner(verbosity=1).run(suite)
                    tests_results.append("flow: {} test: {} result: {}".format(flow['name'], test['name'], result))






# ---START OF SCRIPT
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MainTester)
    unittest.TextTestRunner(verbosity=1).run(suite)
