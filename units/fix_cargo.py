import json

def process_data(unit_data):
    # Iterate and modify the "cargo" field
    cargo = unit_data.get("Cargo") 
    if cargo == None: return

    new_cargo = ""

    # Remove first and last characters from cargo 
    cargo = cargo[1:-1]
    print(cargo)

    # Split by '}{' and add '1,0,1'
    parts = cargo.split('}{')
    for part in parts:
        new_cargo += f"{{{part};1;0;1}}"

    unit_data["Cargo"] = new_cargo

def process_units(units):
    for unit in units:
        data = unit.get("data")
        inner_units = unit.get("units")

        if data != None:
            process_data(data)
        
        if inner_units != None:
            process_units(inner_units)


if __name__ == '__main__':
    # Load the JSON data from ships.json
    with open('ships.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        process_units(data.get("units"))
    
    # Overwrite the file with the modified data
    with open('ships.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)