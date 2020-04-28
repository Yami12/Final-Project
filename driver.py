import os
from appium import webdriver

global_driver_child = None
global_driver_father = None
current_test = None

def initialize(owner_flag ,platformName, platformVersion, deviceName, appPackage, appActivity, apk_file = ""):
    #father in port 5556, child in port 5554
    localhost = '5554'
    if owner_flag == "father":
        localhost = '5556'
    global global_driver_child
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
    global_driver_child = webdriver.Remote('http://localhost:' + localhost +'/wd/hub', desired_caps)


def close_driver():
    global global_driver_child
    global_driver_child.quit()

#     driver.current_activity

#     start_activity("com.example", "ActivityName"); 