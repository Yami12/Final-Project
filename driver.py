'''
This file handles the appium's driver
there is 2 attributes:
global_driver: the appium driver
current_test: the current test that run on the android phone
'''

import os


from appium import webdriver


global_driver = None
global_tests_result = []

requested_flow = None
current_test = None
desired_caps = {}

'''
function:initialize
description: initializes the appium's driver
parameters:
platformName - the phone's OS - in our case only Android
platformVersion - the OS version
deviceName - the android phone 
appPackage - the application name
appActivity - the application's activity name
localhost - the appium's driver host
apk_file - the application's apk file
'''
def initialize(platformName, platformVersion, deviceName, apk_file = ""):

    global global_driver
    global desired_caps
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = platformVersion
    desired_caps['deviceName'] = deviceName
    # Returns abs path relative to this file and not cwd
    if apk_file != "":
        desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__), apk_file))
    else:
        desired_caps['noReset'] = True


def connect_driver(appPackage, appActivity):
    global desired_caps
    global global_driver
    desired_caps['appPackage'] = appPackage
    desired_caps['appActivity'] = appActivity

    global_driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

