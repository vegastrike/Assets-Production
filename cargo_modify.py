import json


def modify_item(item):
    if item.get("categoryname").startswith("Passengers"):
        item["passenger"] = True

    if "Slaves" == item.get("file") or "Pilot" == item.get("file"):
        item["passenger"] = True
        item["slave"] = True
    
    if item.get("categoryname").startswith("upgrades/"):
        item["upgrade"] = True

    if item.get("categoryname").startswith("upgrades/Weapons") or item.get("categoryname").startswith("upgrades/Ammunition"):
        item["weapoon"] = True


if __name__ == '__main__':
    items = []
    upgrades = []
    weapons = []

    jsons = ['master_component_list.json', 'master_part_list.json', 'master_ship_list.json']
    
    for json_file in jsons:
        with open(json_file,'r') as items_file:
            items_str = items_file.read()
            items = json.loads(items_str)

        for item in items:
            modify_item(item)

        with open(json_file, 'w') as units_file:
            json.dump(items, units_file, ensure_ascii=False, indent=4)
      
    print("Success")
