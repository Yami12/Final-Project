'''
this file handles the tests xml file and all the tests operations
'''

import xml.etree.cElementTree as et


'''
function:xml_to_dictionary
description: converts the xml file of tests to list of dictionaries
parameters:
file_name - the name of the xml file
'''
def component_xml_to_dictionary(file_name):
    file = open(file_name)
    file_content = file.read()
    tree = et.fromstring(file_content)
    flowes = tree.findall('flow')#first node in the xml file

    flowes_arr = []
    #go over the all flowes
    for flow in flowes:
        flow_dict = {}
        tests_arr = []
        #go over all the flow's tests
        for tests in flow:
            if tests.tag == 'name':#flow name
                flow_dict['name'] = tests.text
            else:
                for test in tests:# flow's tests
                    test_dict = {}
                    for i in test:
                        test_dict[i.tag] = i.text
                    tests_arr.append(test_dict)
            flow_dict['tests'] = tests_arr
        flowes_arr.append(flow_dict)
    return flowes_arr

def feature_xml_to_dictionary(file_name):
    file = open(file_name,encoding='UTF-8')
    file_content = file.read()
    tree = et.fromstring(file_content)

    tests = tree.findall('test')  # first node in the xml file

    tests_arr = []
    # go over the all flowes
    for test in tests:
        test_dict = {}
        test_dict['name'] = test.text
        for i in test:
            test_dict[i.tag] = i.text
        tests_arr.append(test_dict)
        print(test_dict)
    print(tests_arr)
    return tests_arr

'''
function:dictionary_to_xml
description: converts list of dictionaries to xml file
parameters:
dict - the list of the dictionaries
file_name - the name of the xml file
'''
def dictionary_to_xml(dict, file_name):
    root = et.Element("flowes")
    for flow in dict:
        flow_node = et.SubElement(root, "flow")
        for key in flow.keys():
            if key == 'name':
                et.SubElement(flow_node, key).text = flow[key]
            else:
                tests = et.SubElement(flow_node, "tests")
                for i in flow[key]:
                    test = et.SubElement(tests, "test")
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
        if flow['name'] == flow_name:
            flow['tests'].append(test)#adds the new test
            break
    dictionary_to_xml(flowes_list, 'xml_file.xml')#write to the file


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
        if flow['name'] == flow_name:
            # go over all the flow's tests
            for test in flow['tests']:
                if test['name'] == test_name:
                    flow['tests'].remove(test)#deletes the new test
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
        if flow['name'] == flow_name:
            # go over all the flow's tests
            for test in flow['tests']:
                if test['name'] == test_name:#update test's fields
                    selected = test['type']
                    if selected == 'Button':
                        test['actionType'] = action_or_content
                    elif selected == "Label":
                        test['content'] = action_or_content
                    test['expectedResult'] = expected_result
                    break
                    print(test)
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
        if flow['name'] == flow_name:
            # go over all the flow's tests
            for test in flow['tests']:
                if test['name'] == test_name:
                    return test

