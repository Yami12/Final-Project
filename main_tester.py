import unittest
import driver
from install_child_side import InstallChildSide
from download_app import DownloadApp


class MainTester(unittest.TestCase):
    "Class to run tests against the Chess Free app"


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
        driver.initialize('Android', '8.0.0', 'My HUAWEI', 'com.keepers', 'com.keeper.common.splash.SplashActivity',
                          '4723')
        suite = unittest.TestLoader().loadTestsFromTestCase(InstallChildSide)
        result = unittest.TextTestRunner(verbosity=1).run(suite)


# ---START OF SCRIPT
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MainTester)
    unittest.TextTestRunner(verbosity=1).run(suite)
