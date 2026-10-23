import json
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom

with open("network_data.json", "r") as f:
    api_data = json.load(f)

active_vlans = []
for vlan in api_data["vlans"]:
    if vlan["status"] == "active":
        vlan_dict = {
            "id": vlan["vid"],
            "name": vlan["name"]
        }
        active_vlans.append(vlan_dict)

normalized_data = {
    "device": {
        "hostname": api_data["device"]["name"],
        "site": api_data["device"]["site"]["name"],
        "platform": api_data["device"]["platform"]["name"]
    },
    "vlans": active_vlans
}

with open("normalized_data.yml", "w") as yaml_file:
    yaml.safe_dump(normalized_data, yaml_file, sort_keys=False)

config_elem = ET.Element("config")
vlans_elem = ET.SubElement(config_elem, "vlans")

for vlan in normalized_data["vlans"]:
    vlan_elem = ET.SubElement(vlans_elem, "vlan")
    vlan_id_elem = ET.SubElement(vlan_elem, "vlan-id")
    vlan_id_elem.text = str(vlan["id"])
    vlan_name_elem = ET.SubElement(vlan_elem, "name")
    vlan_name_elem.text = vlan["name"]

xml_bytes = ET.tostring(config_elem)
parsed_xml = minidom.parseString(xml_bytes)
pretty_xml = parsed_xml.toprettyxml(indent="    ")

with open("vlan_config.xml", "w") as xml_file:
    xml_file.write(pretty_xml)

for vlan_node in config_elem.findall("./vlans/vlan"):
    v_id = vlan_node.findtext("vlan-id")
    v_name = vlan_node.findtext("name")
    print(f"VLAN ID: {v_id} | Name: {v_name}")

vlan_20_exists = False
for vlan_node in config_elem.findall("./vlans/vlan"):
    if vlan_node.findtext("vlan-id") == "20":
        vlan_20_exists = True

if vlan_20_exists:
    print("Validation PASSED: VLAN 20 exists.")
else:
    print("Validation FAILED: VLAN 20 does not exist.")

all_valid = True
for vlan_node in config_elem.findall("./vlans/vlan"):
    vid_num = int(vlan_node.findtext("vlan-id"))
    if vid_num < 1 or vid_num > 4094:
        all_valid = False

if all_valid:
    print("VLAN validation PASSED.")
else:
    print("VLAN validation FAILED.")
