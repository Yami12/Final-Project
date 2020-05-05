'''
This file handles the appium's driver
there is 2 attributes:
global_driver: the appium driver
current_test: the current test that run on the android phone
'''

import os
from appium import webdriver

global_driver_child = None
global_driver_father = None
current_test = None
father_desired_caps = {}
child_desired_caps = {}

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
def initialize(owner_flag ,platformName, platformVersion, deviceName, appPackage, appActivity, apk_file = ""):
    #father in port 5556, child in port 4723
    global global_driver_child
    global global_driver_father

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
    desired_caps['adbExecTimeout'] = '200000'
    if owner_flag == "father":
        global father_desired_caps
        father_desired_caps = desired_caps
    else:
        global child_desired_caps
        child_desired_caps = desired_caps
        print(child_desired_caps)
        print("---------",owner_flag)



def initialize_father():
    global global_driver_father
    global_driver_father = webdriver.Remote('http://localhost:4724/wd/hub', father_desired_caps)

def initialize_child():
    global global_driver_child
    global_driver_child = webdriver.Remote('http://localhost:5556/wd/hub', child_desired_caps)



'''
function:close_driver
description: close the appium's driver
'''
def close_driver():
    global global_driver
    global_driver.quit()


