'''
This file handles the appium's driver
there is 2 attributes:
global_driver: the appium driver
current_test: the current test that run on the android phone
'''

import os
import subprocess
from appium import webdriver

global_driver = None
global_tests_result = []
#the results in format: [{name: name_test, results:[[True, 'device lock'], [false, 'command not found']},{...}]

current_test = None
current_app = None
tests_folders_names = ""
desired_caps = {}
sending_time = ""
child_device = ""
father_device = ""
tester_device = ""

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


def connect_driver(appPackage, appActivity):
    global desired_caps
    global global_driver
    desired_caps['appPackage'] = appPackage
    desired_caps['appActivity'] = appActivity
    print("connecting to appium server...")
    global_driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


def get_device_version(device):
    print(device)
    process = subprocess.Popen(['adb', '-s', device, 'shell', 'getprop', 'ro.build.version.release'],
                               stdout=subprocess.PIPE)
    print(str(process.stdout.read())[2:])
    device_ver = str(process.stdout.read())[2:].split("\\r\\n")[0]
    process.kill()
    print("get device version: ", device_ver)

    return device_ver


    #
    # devices = []
    #
    # devices_udid = []
    # process = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE)
    # a = str(process.stdout.read())
    # print(a)
    # udids = str(a).split('\\r\\n')
    #
    # for i in range(2):
    #     device = {}
    #     device[sl.DEVICE_UDID] = udids[i+1].split("\\tdevice")[0]
    #     process = subprocess.Popen(['adb', '-s', device[sl.DEVICE_UDID], 'shell', 'getprop', 'ro.build.version.release'], stdout=subprocess.PIPE)
    #     device[sl.DEVICE_VERSION] = str(process.stdout.read())[2:].split("\\r\\n")[0]
    #     device[sl.DEVICE_PLATFORM] = sl.DEVICE_OS
    #     devices.append(device)
    #     print(device)
    # return devices