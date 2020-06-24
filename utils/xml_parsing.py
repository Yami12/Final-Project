'''
this file handles the tests xml file and all the tests operations
'''

import xml.etree.cElementTree as et
from utils import string_list as sl
import os

parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# -------------------------------------features------------------------------------

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

def tests_xml_to_dictionary(file_name):
    file = open(os.path.join(parentDirectory, sl.XML_FOLDER, file_name),encoding='utf8')
    file_content = file.read()
    tree = et.fromstring(file_content)
    if file_name == sl.APPS_FILE or file_name == sl.REMOVAL_FILE:
        tests = tree.findall(sl.app)  # first node in the xml file
    elif file_name == sl.WEB_FILTERING_FILE:
        tests = tree.findall(sl.BROWSER)
    else:
        tests = tree.findall(sl.TEST)  # first node in the xml file


    tests_arr = []
    # go over the all the apps
    for test in tests:
        test_dict = {}
        steps_arr = []
        for i in test:
            if not i.tag == sl.STEPS:
                test_dict[i.tag] = i.text
            else:
                for step in i:  # app's steps
                    step_dict = {}
                    for j in step:
                        step_dict[j.tag] = j.text
                    steps_arr.append(step_dict)
            test_dict['steps'] = steps_arr
        tests_arr.append(test_dict)
    return tests_arr


# -------------------------------------components------------------------------------



'''
function:tests_dictionary_to_xml
description: converts list of dictionaries to xml file
parameters:
dict - the list of the dictionaries
file_name - the name of the xml file
'''
def tests_dictionary_to_xml(dict, file_name):
    root = et.Element(sl.TESTS)
    for test in dict:
        test_node = et.SubElement(root, sl.TEST)
        for key in test.keys():
            if key == sl.STEPS:
                steps = et.SubElement(test_node, sl.STEPS)
                for i in test[key]:
                    step = et.SubElement(steps, sl.STEP)
                    for j in i.keys():
                        et.SubElement(step, j).text = i[j]
            else:
                et.SubElement(test_node, key).text = test[key]

    tree = et.ElementTree(root)
    tree.write(file_name)


def delete_test(test_name, file_name):
    tests = tests_xml_to_dictionary(file_name)
    for test in tests:
        if test[sl.TEST_NAME] == test_name:
            tests.remove(test)
            break
    tests_dictionary_to_xml(test, file_name)


def delete_step_from_test(test_name, step_to_delete, file_name):
    tests = tests_xml_to_dictionary(file_name)
    for test in tests:
        if test[sl.TEST_NAME] == test_name:
            for step in test[sl.STEPS]:
                if ((step[sl.TYPE_STEP] == step_to_delete[sl.TYPE_STEP]) and (
                    step[sl.ID_STEP] == step_to_delete[sl.ID_STEP]) and (
                    step[sl.ACTION_STEP] == step_to_delete[sl.ACTION_STEP]) and (
                    step[sl.CONTENT_STEP] == step_to_delete[sl.CONTENT_STEP])):
                        test[sl.STEPS].remove(step)
                        break
    tests_dictionary_to_xml(tests, file_name)


def add_new_test(test, file_name):
    tests = tests_xml_to_dictionary(file_name)
    tests.append(test)
    tests_dictionary_to_xml(tests, file_name)

def update_tests(test_to_update, old_step, new_step, file_name):
    tests = tests_xml_to_dictionary(file_name)
    for test in tests:
        if test[sl.TEST_NAME] == test_to_update[sl.TEST_NAME]:
            for step in test[sl.STEPS]:
                if ((step[sl.TYPE_STEP] == old_step[sl.TYPE_STEP]) and (
                    step[sl.ID_STEP] == old_step[sl.ID_STEP]) and (
                    step[sl.ACTION_STEP] == old_step[sl.ACTION_STEP]) and (
                    step[sl.CONTENT_STEP] == old_step[sl.CONTENT_STEP])):
                        step = new_step
                        break

    tests_dictionary_to_xml(tests, file_name)
