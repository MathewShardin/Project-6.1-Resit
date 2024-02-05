from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from lxml import etree
from xml.etree import ElementTree
from src.base_application.api.api_utils import validate_member_xml

root = Element("member")

name_element = SubElement(root, "name")
name_element.text = "Test"

email_element = SubElement(root, "email")
email_element.text = "xmlvalid@gmail.com"

# phone_element = SubElement(root, "phone")
# phone_element.text = "+1232554"

# xml_string = tostring(root, encoding="utf-8").decode('utf-8')

xml_string = tostring(root, encoding="utf-8")
xml_pretty_string = minidom.parseString(xml_string).toprettyxml(indent="  ")
files = {'file': ('data.xml', xml_pretty_string)}

xml_file = files["file"][1]
print(xml_file)
xml_obj = ElementTree.fromstring(xml_string)
print(xml_obj)
# xml_file_pretty = tostring(xml_file, encoding="utf-8")
# print(xml_file_pretty)
# xml_file_string = minidom.parseString(xml_string).toprettyxml(indent="  ")
name = xml_obj.findtext('name')
print(name)



print(validate_member_xml(xml_file))

# if not validate_member_xml(xml_string):
#     print("Failed Validation")
