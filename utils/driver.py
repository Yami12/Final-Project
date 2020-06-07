'''
This file handles the appium's driver
there is 2 attributes:
global_driver: the appium driver
current_test: the current test that run on the android phone
'''

import os
import subprocess

from appium import webdriver
from utils import string_list as sl

global_driver = None
global_tests_result = []

requested_flow = None
current_test = None
current_s_network = None
desired_caps = {}
sending_time = ""
child_device = ""
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
def initialize(platformName, platformVersion, udid, apk_file = ""):

    global global_driver
    global desired_caps
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = platformVersion
    desired_caps['udid'] = udid
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

    global_driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


def identify_connected_device():
    devices = []

    devices_udid = []
    process = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE)
    udids = str(process.stdout.read()).split('\\')
    devices_udid.append(udids[2][1:])
    devices_udid.append(udids[5][1:])
    print(devices_udid)
    # if len(devices_udid) != 2:
    #     return False

    for i in range(len(devices_udid)):
        device = {}
        device[sl.DEVICE_UDID] = devices_udid[i]
        process = subprocess.Popen(['adb', '-s', device[sl.DEVICE_UDID], 'shell', 'getprop', 'ro.build.version.release'], stdout=subprocess.PIPE)
        device[sl.DEVICE_VERSION] = str(process.stdout.read())[2:5]
        device[sl.DEVICE_PLATFORM] = sl.DEVICE_OS
        devices.append(device)
        print(device)
    return devices