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





if __name__ == '__main__':
    flowes=xml_to_dictionary("xml_file.xml")
    print("xml_file:\n",flowes)
    dictionary_to_xml(flowes,"output_1.xml")