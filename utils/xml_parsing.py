'''
this file handles the tests xml file and all the tests operations
'''

import xml.etree.cElementTree as et
from utils import string_list as sl
import os

parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
# -------------------------------------devices------------------------------------

def devices_xml_to_dictionary(file_name):
    file = open(os.path.join(parentDirectory, sl.XML_FOLDER, file_name))
    file_content = file.read()
    tree = et.fromstring(file_content)
    devices = tree.findall(sl.DEVICE)  # first node in the xml file

    devices_arr = []
    # go over the all tests
    for device in devices:
        device_dict = {}
        device_dict[sl.DEVICE_NAME] = device.text
        for i in device:
            device_dict[i.tag] = i.text
        devices_arr.append(device_dict)
    return devices_arr

def device_dictionary_to_xml(dict, file_name):
    root = et.Element(sl.DEVICES)
    for device in dict:
        device_node = et.SubElement(root, sl.DEVICE)
        for key in device.keys():
            et.SubElement(device_node, key).text = device[key]

    tree = et.ElementTree(root)
    tree.write(file_name)


def add_new_device(device, file_name):
    devices_list = devices_xml_to_dictionary(file_name)#parse the file to list of dictionaries
    devices_list.append(device)
    device_dictionary_to_xml(devices_list, file_name)#write to the file


# -------------------------------------features------------------------------------

def feature_xml_to_dictionary(file_name):
    os.chdir("..")
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
    file = open(os.path.join(parentDirectory, sl.XML_FOLDER, file_name))
    file_content = file.read()
    tree = et.fromstring(file_content)
    if file_name == sl.NETWORKS_FILE:
        tests = tree.findall(sl.SOCIAL_NETWORK)  # first node in the xml file
    else:
        tests = tree.findall(sl.TEST)  # first node in the xml file


    tests_arr = []
    # go over the all the networks
    for test in tests:
        test_dict = {}
        steps_arr = []
        for i in test:
            if not i.tag == sl.STEPS:
                test_dict[i.tag] = i.text
            else:
                for step in i:  # network's steps
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

    tests_dictionary_to_xml(tests, file_name )
#
# '''
# function: add_new_test_to_flow
# description: adds new test to the given flow and writes it to the xml file
# parameters:
# flow_name - the flow to add the test to
# test - the test to add
# file_name - the name of the xml file
# '''
# #TODO add test_name in order to know where to locate the new test
# def add_new_test_to_flow(flow_name, test, file_name):
#     flowes_list=tests_xml_to_dictionary(file_name)#parse the file to list of dictionaries
#     #go over all the flowes
#     for flow in flowes_list:
#         #go over all the flow's tests
#         if flow[sl.FLOW_NAME] == flow_name:
#             flow[sl.TESTS].append(test)#adds the new test
#             break
#     tests_dictionary_to_xml(flowes_list, file_name)#write to the file
#
#
# '''
# function: delete_test_from_flow
# description: deletes the given test from the given flow and uptate it in the xml file
# parameters:
# flow_name - the flow to delete the test from
# test_name - the test's name to delete
# file_name - the name of the xml file
# '''
# def delete_test_from_flow(flow_name, test_name, file_name):
#     flowes_list = tests_xml_to_dictionary(file_name)#parse the file to list of dictionaries
#     for flow in flowes_list:
#         #go over all the flowes
#         if flow[sl.FLOW_NAME] == flow_name:
#             # go over all the flow's tests
#             for test in flow[sl.TESTS]:
#                 if test[sl.TEST_NAME] == test_name:
#                     flow[sl.TESTS].remove(test)#deletes the new test
#                     break
#             break
#     tests_dictionary_to_xml(flowes_list, file_name)#write to the file
#
# '''
# function: update_test_in_flow
# description: update the given test from the given flow and uptate it in the xml file
# parameters:
# flow_name - the flow to update the test from
# test_name - the test's name to update
# expected_result - field to update
# action_or_content - field to update
# file_name - the name of the xml file
# '''
# def update_test_in_flow(flow_name, test_name, expected_result, action_or_content, file_name):
#     flowes_list = tests_xml_to_dictionary(file_name)
#     for flow in flowes_list:
#         # go over all the flowes
#         if flow[sl.FLOW_NAME] == flow_name:
#             # go over all the flow's tests
#             for test in flow[sl.TESTS]:
#                 if test[sl.TEST_NAME] == test_name:#update test's fields
#                     selected = test[sl.TEST_TYPE]
#                     if selected == sl.BUTTON:
#                         test[sl.TEST_ACTION_TYPE] = action_or_content
#                     elif selected == sl.LABEL:
#                         test[sl.TEST_CONTENT] = action_or_content
#                     test[sl.TEST_EXPECTED_RES] = expected_result
#                     break
#             break
#     tests_dictionary_to_xml(flowes_list, file_name)#write to the file
#
#
# '''
# function: return_test
# description: return fields of the given test
# parameters:
# flow_name - the flow's test
# test_name - the test's name to return
# file_name - the name of the xml file
# '''
# def return_test(flow_name, test_name, file_name):
#     flowes_list = tests_xml_to_dictionary(file_name)
#     for flow in flowes_list:
#         # go over all the flowes
#         if flow[sl.FLOW_NAME] == flow_name:
#             # go over all the flow's tests
#             for test in flow[sl.TESTS]:
#                 if test[sl.TEST_NAME] == test_name:
#                     return test