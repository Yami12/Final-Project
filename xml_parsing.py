import xml.etree.cElementTree as et


# parse xml file to list of dictionaries
file = open("xml_file.xml")
content = file.read()
tree=et.fromstring(content)
dict = [{item.tag: item.text for item in ch} for ch in tree.findall('test')]
print(dict)


#parse list of dictionaries to xml file
root = et.Element("buttonTests")
doc = et.SubElement(root, "test")
for dic in dict:
    for key in  dic.keys():
        et.SubElement(doc, key).text = dic[key]
tree = et.ElementTree(root)
tree.write("output.xml")