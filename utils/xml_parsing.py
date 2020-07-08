'''
this file handles the tests and apps xml file
'''

import xml.etree.cElementTree as et
import os

from utils import string_list as sl

parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

"""
    function: feature_xml_to_dictionary
    description: returns all the features tests from the xml file
"""
def feature_xml_to_dictionary(file_name):
    file = open(os.path.join(parentDirectory, sl.XML_FOLDER, file_name))
    file_content = file.read()
    tree = et.fromstring(file_content)

    tests = tree.findall(sl.TEST)  # first node in the xml file

    tests_arr = []
    # go over the all tests
    for test in tests:
        test_dict = {}
        test_dict[sl.TEST_NAME] = test.text
        for i in test:
            test_dict[i.tag] = i.text
        tests_arr.append(test_dict)
    return tests_arr

"""
    function: tests_xml_to_dictionary
    description: returns all the tests steps (components tests and apps files)
"""
def tests_xml_to_dictionary(file_name):
    file = open(os.path.join(parentDirectory, sl.XML_FOLDER, file_name),encoding='utf8')
    file_content = file.read()
    tree = et.fromstring(file_content)
    if file_name == sl.APPS_FILE:
        tests = tree.findall(sl.app)  # first node in the xml file
    else:
        tests = tree.findall(sl.TEST)  # first node in the xml file

    tests_arr = []
    # go over the all the apps
    for test in tests:
        test_dict = {}
        for i in test:
            if not i.tag == sl.STEPS and not i.tag == sl.REMOVAL_STEPS:
                test_dict[i.tag] = i.text
            else:
                steps_arr = []
                for step in i:  # app's steps
                    step_dict = {}
                    for j in step:
                        step_dict[j.tag] = j.text
                    steps_arr.append(step_dict)
                test_dict[i.tag] = steps_arr
        tests_arr.append(test_dict)
    return tests_arr
