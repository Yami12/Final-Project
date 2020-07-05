'''
This file handles the appium's driver and the current test details
'''

import os
import subprocess
from appium import webdriver

global_driver = None
global_tests_result = []
current_test = None
tests_folders_names = ""
desired_caps = {}
sending_time = ""
child_device = ""
father_device = ""
tester_device = ""
test_result = ""

'''
    function:initialize
    description: initializes the appium's driver according to the device details
'''
def initialize(device, apk_file = ""):

    global desired_caps
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = get_device_version(device)
    desired_caps['udid'] = device
    desired_caps['adbExecTimeout'] = '500000'
    # Returns abs path relative to this file and not cwd
    if apk_file != "":
        desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__), apk_file))
    else:
        desired_caps['noReset'] = True

"""
    function: connect_driver
    description: connect to appuium server according to device and app details
"""
def connect_driver(appPackage, appActivity):
    global desired_caps
    global global_driver
    desired_caps['appPackage'] = appPackage
    desired_caps['appActivity'] = appActivity
    global_driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


"""
    function: get_device_version
    description: return the device version
"""
def get_device_version(device):
    print(device)
    process = subprocess.Popen(['adb', '-s', device, 'shell', 'getprop', 'ro.build.version.release'],
                               stdout=subprocess.PIPE)
    print(str(process.stdout.read())[2:])
    device_ver = str(process.stdout.read())[2:].split("\\r\\n")[0]

    process.kill()
    return device_ver
