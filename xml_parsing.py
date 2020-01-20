import xml.etree.cElementTree as et

#
# parse xml file to list of dictionaries
#
def xml_to_dictionary(file_name):
    file = open(file_name)
    file_content = file.read()
    tree = et.fromstring(file_content)
    flowes = tree.findall('flow')#first node in the xnl file

    flowes_arr = []

    for flow in flowes:
        flow_dict = {}
        tests_arr = []
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

#
#parse list of dictionaries to xml file
#
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



#TODO add test_name in order to know where to locate the new test
def add_new_test_to_flow(flow_name, test, file_name):
    flowes_list=xml_to_dictionary(file_name)
    for flow in flowes_list:
        if flow['name'] == flow_name:
            flow['tests'].append(test)
            break
    dictionary_to_xml(flowes_list, 'xml_file.xml')


def delete_test_from_flow(flow_name, test_name, file_name):
    flowes_list = xml_to_dictionary(file_name)
    for flow in flowes_list:
        if flow['name'] == flow_name:
            for test in flow['tests']:
                if test['name'] == test_name:
                    flow['tests'].remove(test)
                    break
            break
    dictionary_to_xml(flowes_list, 'xml_file.xml')


def update_test_in_flow(flow_name, test, file_name):
    return


def return_test(flow_name, test_name, file_name):
    flowes_list = xml_to_dictionary(file_name)
    for flow in flowes_list:
        if flow['name'] == flow_name:
            for test in flow['tests']:
                if test['name'] == test_name:
                    return test


if __name__ == '__main__':
    flowes=xml_to_dictionary("xml_file.xml")
    print("xml_file:\n",flowes)
    dictionary_to_xml(flowes,"output_1.xml")
