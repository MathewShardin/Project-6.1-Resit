from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from lxml import etree

from src.base_application.api.api_utils import validate_member_xml

root = Element("member")

name_element = SubElement(root, "name")
name_element.text = "Test"

email_element = SubElement(root, "email")
email_element.text = "xmlvalid@gmail.com"

# phone_element = SubElement(root, "phone")
# phone_element.text = "+1232554"

xml_string = tostring(root, encoding="utf-8").decode('utf-8')

print(validate_member_xml(xml_string))

# if not validate_member_xml(xml_string):
#     print("Failed Validation")
