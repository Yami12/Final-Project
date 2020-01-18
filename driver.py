import os
from appium import webdriver

global_driver = None
current_test = None

def initialize(platformName, platformVersion, deviceName, appPackage, appActivity, localhost, apk_file = ""):
    global global_driver
    desired_caps = {}
    desired_caps['platformName'] = platformName
    desired_caps['platformVersion'] = platformVersion
    desired_caps['deviceName'] = deviceName
    # Returns abs path relative to this file and not cwd
    if apk_file != "":
        desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__), apk_file))
    else:
        desired_caps['noReset'] = 'true'
    desired_caps['appPackage'] = appPackage
    desired_caps['appActivity'] = appActivity
    global_driver = webdriver.Remote('http://localhost:' + localhost +'/wd/hub', desired_caps)


def close_driver():
    global global_driver
    global_driver.quit()

#     driver.current_activity

#     start_activity("com.example", "ActivityName"); ‏

