# Convert weapon_list.xml to weapons.json

import json
import xml.etree.ElementTree as et

weapon_xml = et.parse('weapon_list.xml')
root = weapon_xml.getroot()

string_keys = ["type","name","mountsize","file","soundwav"]
weapons = []
for elem in root:
    weapon_dict = {}
    weapon_dict['type'] = elem.tag
    weapon_dict.update(elem.attrib)
    
    for child in elem:
        prefix = child.tag
        for key,value in child.attrib.items():
            if key in string_keys: 
                weapon_dict[prefix + '.' + key] = value
            else:
                weapon_dict[prefix + '.' + key] = float(value)
    
    weapons.append(weapon_dict)
          
json_object = json.dumps(weapons, indent = 4)
with open("weapons.json", "w") as json_file:
    json_file.write(json_object)
print(json_object)
