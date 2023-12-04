import requests
import xml.etree.ElementTree as ET
from src.base_application import api_server_ip
from src.base_application.api.api_utils import validate_member_xml
from xml.etree.ElementTree import Element, SubElement, tostring

root = Element('member')
name_xml = SubElement(root, 'name')
name_xml.text = "Test"
email_xml = SubElement(root, 'email')
email_xml.text = "XML@gmail.com"
xml_payload = tostring(root, encoding='unicode', method='xml')
print(type(xml_payload))
root = ET.fromstring(xml_payload)
print(type(root))
# Make sure the schema is properly encoded to be validated
xml_str = ET.tostring(root)
email = str(root.find('email').text)
print(email)

if not validate_member_xml(xml_str):
    print("Validation error")




url = api_server_ip + '/api/insertMemberSQL'
headers = {'Content-Type': 'application/xml'}
response = requests.post(url, json=xml_payload, headers=headers)