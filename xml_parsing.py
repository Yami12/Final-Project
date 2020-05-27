'''
this file handles the tests xml file and all the tests operations
'''

import xml.etree.cElementTree as et
import string_list as sl


# -------------------------------------devices------------------------------------

def devices_xml_to_dictionary(file_name):
    file = open(file_name)
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
    file = open(file_name,encoding='UTF-8')
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

def social_network_xml_to_dictionary(file_name):
    file = open(file_name)
    file_content = file.read()
    tree = et.fromstring(file_content)
    s_network = tree.findall(sl.SOCIAL_NETWORK)  # first node in the xml file

    networks_arr = []
    # go over the all the networks
    for network in s_network:
        network_dict = {}
        steps_arr = []
        for i in network:
            if not i.tag == sl.STEPS:
                network_dict[i.tag] = i.text
            else:
                for step in i:  # network's steps
                    step_dict = {}
                    for j in step:
                        step_dict[j.tag] = j.text
                    steps_arr.append(step_dict)
            network_dict['steps'] = steps_arr
        networks_arr.append(network_dict)
    return networks_arr


# -------------------------------------components------------------------------------

def component_xml_to_dictionary(file_name):
    file = open(file_name)
    file_content = file.read()
    tree = et.fromstring(file_content)
    flowes = tree.findall(sl.FLOW)#first node in the xml file

    flowes_arr = []
    #go over the all flowes
    for flow in flowes:
        flow_dict = {}
        tests_arr = []
        #go over all the flow's tests
        for tests in flow:
            if tests.tag == sl.FLOW_NAME:#flow name
                flow_dict[sl.FLOW_NAME] = tests.text
            else:
                for test in tests:# flow's tests
                    test_dict = {}
                    for i in test:
                        test_dict[i.tag] = i.text
                    tests_arr.append(test_dict)
            flow_dict[sl.TESTS] = tests_arr
        flowes_arr.append(flow_dict)
    return flowes_arr

'''
function:dictionary_to_xml
description: converts list of dictionaries to xml file
parameters:
dict - the list of the dictionaries
file_name - the name of the xml file
'''
def dictionary_to_xml(dict, file_name):
    root = et.Element(sl.FLOWES)
    for flow in dict:
        flow_node = et.SubElement(root, sl.FLOW)
        for key in flow.keys():
            if key == sl.FLOW_NAME:
                et.SubElement(flow_node, key).text = flow[key]
            else:
                tests = et.SubElement(flow_node, sl.TESTS)
                for i in flow[key]:
                    test = et.SubElement(tests, sl.TEST)
                    for j in i.keys():
                        et.SubElement(test, j).text = i[j]

    tree = et.ElementTree(root)
    tree.write(file_name)


'''
function: add_new_test_to_flow
description: adds new test to the given flow and writes it to the xml file
parameters:
flow_name - the flow to add the test to
test - the test to add
file_name - the name of the xml file
'''
#TODO add test_name in order to know where to locate the new test
def add_new_test_to_flow(flow_name, test, file_name):
    flowes_list=component_xml_to_dictionary(file_name)#parse the file to list of dictionaries
    #go over all the flowes
    for flow in flowes_list:
        #go over all the flow's tests
        if flow[sl.FLOW_NAME] == flow_name:
            flow[sl.TESTS].append(test)#adds the new test
            break
    dictionary_to_xml(flowes_list, file_name)#write to the file


'''
function: delete_test_from_flow
description: deletes the given test from the given flow and uptate it in the xml file
parameters:
flow_name - the flow to delete the test from
test_name - the test's name to delete
file_name - the name of the xml file
'''
def delete_test_from_flow(flow_name, test_name, file_name):
    flowes_list = component_xml_to_dictionary(file_name)#parse the file to list of dictionaries
    for flow in flowes_list:
        #go over all the flowes
        if flow[sl.FLOW_NAME] == flow_name:
            # go over all the flow's tests
            for test in flow[sl.TESTS]:
                if test[sl.TEST_NAME] == test_name:
                    flow[sl.TESTS].remove(test)#deletes the new test
                    break
            break
    dictionary_to_xml(flowes_list, file_name)#write to the file

'''
function: update_test_in_flow
description: update the given test from the given flow and uptate it in the xml file
parameters:
flow_name - the flow to update the test from
test_name - the test's name to update
expected_result - field to update
action_or_content - field to update
file_name - the name of the xml file
'''
def update_test_in_flow(flow_name, test_name, expected_result, action_or_content, file_name):
    flowes_list = component_xml_to_dictionary(file_name)
    for flow in flowes_list:
        # go over all the flowes
        if flow[sl.FLOW_NAME] == flow_name:
            # go over all the flow's tests
            for test in flow[sl.TESTS]:
                if test[sl.TEST_NAME] == test_name:#update test's fields
                    selected = test[sl.TEST_TYPE]
                    if selected == sl.BUTTON:
                        test[sl.TEST_ACTION_TYPE] = action_or_content
                    elif selected == sl.LABEL:
                        test[sl.TEST_CONTENT] = action_or_content
                    test[sl.TEST_EXPECTED_RES] = expected_result
                    break
            break
    dictionary_to_xml(flowes_list, file_name)#write to the file


'''
function: return_test
description: return fields of the given test
parameters:
flow_name - the flow's test
test_name - the test's name to return
file_name - the name of the xml file
'''
def return_test(flow_name, test_name, file_name):
    flowes_list = component_xml_to_dictionary(file_name)
    for flow in flowes_list:
        # go over all the flowes
        if flow[sl.FLOW_NAME] == flow_name:
            # go over all the flow's tests
            for test in flow[sl.TESTS]:
                if test[sl.TEST_NAME] == test_name:
                    return test