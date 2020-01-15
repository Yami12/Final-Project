import xml.etree.cElementTree as et


# parse xml file to list of dictionaries
file = open("xml_file.xml")
content = file.read()
tree=et.fromstring(content)
flowes=tree.findall('flow')


flowes_=[]

for flow in flowes:
    flow_ = {}
    tests_ = []
    for tests in flow:
        if tests.tag == 'name':
            flow_['name'] = tests.text
        else:
            for test in tests:
                test_ = {}
                for i in test:
                    test_[i.tag] = i.text
                tests_.append(test_)
        flow_['tests']=tests_
    flowes_.append(flow_)
print(flowes_)
            # tests = [{item.tag: item.text for item in ch} for test in flow]
#
# #parse list of dictionaries to xml file
root = et.Element("flowes")
for flow in flowes:
    doc = et.SubElement(root, "flow")
    for key in  flow.keys():
        if key == 'name':
            et.SubElement(doc, key).text = flow[key]
        else:
            doc_=et.SubElement(doc, "tests")
            for i in flow[key]:
                test=et.SubElement(doc_, "test")
                for j in i.keys():
                    et.SubElement(test, j).text = i[j]

tree = et.ElementTree(root)
tree.write("output.xml")