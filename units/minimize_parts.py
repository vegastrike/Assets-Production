import json
import sys
import os

KEY  = 'Key'
NAME = 'Name'
BLANK = 'blank'

delete_array = ['box', 'box.blank', 'box.template']
delete_keys = ['Moment_Of_Inertia']

minimize_array = [('armor', ['armor_front', 'armor_rear','armor_left', 'armor_right']),
                  ('shield_strength',['shield_front', 'shield_back','shield_left', 'shield_right']),
                  ('accel', ['Left_Accel',
                            'Right_Accel',
                            'Top_Accel',
                            'Bottom_Accel'])
                 ]

force_array = [(['armor_front', 'armor_back','armor_left', 'armor_right'], 
                ['Armor_Front_Top_Right', 'Armor_Front_Top_Left',
                'Armor_Front_Bottom_Right', 'Armor_Front_Bottom_Left',
                'Armor_Back_Top_Right', 'Armor_Back_Top_Left',
                'Armor_Back_Bottom_Right',
                'Armor_Back_Bottom_Left'], 'armor'),
                (['shield_front', 'shield_back','shield_left', 'shield_right'],
                ['Shield_Front_Top_Right', 'Shield_Back_Top_Left',
                 'Shield_Front_Bottom_Right', 'Shield_Front_Bottom_Left'], 'shield')]

ship_defaults = {"Object_Type": "Vessel",
        "Hud_Functionality": "1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1",
        "Max_Hud_Functionality": "1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1",
        "Lifesupport_Functionality" : "1",
        "Max_Lifesupport_Functionality": "1",
        "Comm_Functionality": "1",
        "Max_Comm_Functionality": "1",
        "FireControl_Functionality": "1",
        "Max_FireControl_Functionality": "1",
        "SPECDrive_Functionality": "1",
        "Max_SPECDrive_Functionality" : "1",
        "Tractorability": "pPiI",
        "Jump_Drive_Delay": "1",
        "Sound": ";;;;;;"
}

# Utils
def get_ship_by_key(key, units):
    for unit in units:
        if unit[KEY] == key:
            return unit
        
    return None

def get_ship_by_name_and_variant(name, variant, units):
    for unit in units:
        if unit[KEY].endswith(variant) and unit[NAME] == name:
            return unit
        
    return None

def delete_ship_by_key(key, units):
    for unit in units:
        if unit[KEY] == key:
            units.remove(unit)
            return
        

# Convert old armor/shield to new format
def force_minimize_shield_and_armor(unit, new_keys, old_keys, min_key):
    sum_value = 0
    facets = 0
    for old_key in old_keys:
        if old_key not in unit:
            continue
        
        sum_value += int(round(float(unit[old_key])))
        facets += 1 
    

    if facets == 2:
        unit[new_keys[0]] = unit[new_keys[1]] = str(sum_value / 2)
    elif facets == 4:
        unit[new_keys[0]] = unit[new_keys[1]] = str(sum_value / 4)
        unit[new_keys[2]] = unit[new_keys[3]] = str(sum_value / 4)
    elif facets == 8:
        unit[new_keys[0]] = unit[new_keys[1]] = str(sum_value / 4)
        unit[new_keys[2]] = unit[new_keys[3]] = str(sum_value / 4)
    elif facets == 0:
        # Nothing to do
        pass
    else:
        print(unit)
        print('\n')
        print(f"Illegal number of facets {facets} in force_minimize_shield_and_armor for {unit['Key']}")
        sys.exit(1)

    if facets == 8:
        facets = 4

    # Try and minimize to one value
    if facets == 2:
        if unit[new_keys[0]] == unit[new_keys[1]]:
            # Minimize new keys. We have a single value
            unit[min_key] = unit[new_keys[0]]
            del(unit[new_keys[0]])
            del(unit[new_keys[1]])

    elif facets == 4:
        if unit[new_keys[0]] == unit[new_keys[1]] and unit[new_keys[0]] == unit[new_keys[2]] and unit[new_keys[0]] == unit[new_keys[3]]: 
            unit[min_key] = unit[new_keys[0]]
            # Minimize new keys. We have a single value
            for new_key in new_keys:
                del(unit[new_key])

    # We got to the end, we can minimize
    for old_key in old_keys:
        if old_key in unit:
            del(unit[old_key])

    # Add shield facets
    if min_key == 'shield' and (facets == 2 or facets == 4):
        unit['shield_facets'] = str(facets)
    
    if min_key in unit and unit[min_key] == '0.0':
        del(unit[min_key])
                   

def minimize_some_values(unit, new_key, old_keys):
    old_value = None
    for old_key in old_keys:
        if old_key not in unit:
            return
        
        temp = unit[old_key]        
        temp = int(round(float(temp)))
        
        if temp != old_value and old_value != None:
            # values don't match, exit
            print(f"{unit['Key']} has inconsistent {old_key}")
            return
        
        old_value = temp
        
    # We got to the end, we can minimize
    for old_key in old_keys:
        del(unit[old_key])
        
    # Add new key
    if old_value != 0:
        unit[new_key] = str(old_value)
    


def minimize(units, upgrades, base_template):
    for unit in units:
        key = unit['Key']

        if key == 'generic_cargo':
            print('cargo')
        
        # Delete keys
        for key_to_delete in delete_keys:
            if key_to_delete in unit:
                del unit[key_to_delete]
        
        # clean values
        for k,v in unit.items():
            if v == "TRUE":
                unit[k] = "1"
            elif v == "FALSE":
                unit[k] = "0"
        
        # Base Template - apply to all items
        for k,v in base_template.items():
            if k in unit and v == unit[k]:
                del unit[k]
        
        # Force minimize shields and armor
        for force_minimize in force_array:
            new_keys = force_minimize[0]
            old_keys = force_minimize[1]
            min_key = force_minimize[2]
            force_minimize_shield_and_armor(unit, new_keys, old_keys, min_key)

        for minimize_values in minimize_array:
            new_key = minimize_values[0]
            old_keys = minimize_values[1]
            minimize_some_values(unit, new_key, old_keys)
            
        if not is_ship(unit):
            # Only apply base template
            continue
        
        
        # TODO - enable this when we support it in engine
        #cargo_stats = generate_cargo(unit, upgrades)
        
        #for k,v in cargo_stats.items():
            #if k in unit and v == unit[k]:
                #del unit[k]
        
                
        

def is_ship(unit):
    key = unit['Key']
    
    exclude_list = []
    exclude_key_list = ['Base', 'turret', 'Milspec_Package', 'Belt', 'Field', 'Jump', 'Asteroid', 'asteroid', 'cargo']
    exclude_roles = ['BOMB', 'HEAVYMISSILE', 'MISSILE', 'MINE', 'POINTDEF']
    include_list_non_zero = ['Hull', 'Fuel_Capacity', 'Forward_Accel']
    
    for exclude in exclude_list:
        if exclude in unit:
            return False
       
    for exclude in exclude_key_list:
        if exclude in key:
            return False
        
    if 'Combat_Role' in unit:
        for exclude in exclude_roles:
            role = unit['Combat_Role']
            if exclude == role:
                return False
        
    for include in include_list_non_zero:
        if include not in unit:
            return False
        
        value = float(unit[include])
        if value == 0:
            return False
    
    return True

# Go over units and extract all units with __upgrades into a separate list
# Remove some keys in the first line as well
def generate_upgrades(units):
    exclude_list = ['Key', 'Name', 'Object_Type', 'Textual_Description', 'Moment_Of_Inertia', 'Mounts']
    upgrades = {}
    for unit in units:
        key = unit['Key']
        if key.endswith('__upgrades'):
            key = key.replace('__upgrades','')
            
            unit_copy = dict(unit)
            for ex in exclude_list:
                if ex in unit_copy:
                    del unit_copy[ex]
            
            if len(unit_copy) > 1: # Always has mass
                upgrades[key] = unit_copy
            
    return upgrades

# First you group ships with below, and then you stack minimized ships with stack_ships below that
def group_ships(units):
    variants = ['blank', 'rg','rgspec', 'stock', 'civvie', 'milspec', 'HSspec', 'merchant', 'puristspec', 'salvage', 'shaperspec', 'escort', 'iso', 'isospec', 'hunter', 'hunterspec', 'tutorial', 'highbornspec', 'template', 'klkkspec', 'begin']
    
    ships = {}
    for unit in units:
        if not is_ship(unit):
            continue
        
        key = unit['Key']
        name = unit['Name'] #if 'Name' in unit else ''
        
        
        ship = []
        if name in ships:
            ship = ships[name]
        else:
            ships[name] = ship
        
        if '.' not in key:
            ship.insert(0, '') 
            continue
        
        for variant in variants:
            if key.endswith(variant):
                ship.append(variant)
                continue
    
    return ships

def stack_ships(units, ships):
    # This data structure conforms to the ships.json file
    # It is a recursive json object in the format of:
    # obj = {
    #   data = {ship stats},
    #   units = [obj]
    min_root_data = ship_defaults
    min_root_units = []
    min_root_object = {'data': min_root_data, 'units': min_root_units}
    
    for name, variants in ships.items():
        min_data = {}
        min_units = []
        min_object = {'data': min_data, 'units': min_units}
        min_root_units.append(min_object)
        
        # Without blank we have nothing to minimize against
        if BLANK not in variants:
            print(f"Blank not found for {name} in variants")
            continue
        
        # First get blank
        blank_unit = dict(get_ship_by_name_and_variant(name, BLANK, units))
        if blank_unit == None:
            print(f"Blank not found for {name} in units")
            sys.exit(1)
            continue
        
        # Remove defaults from blank
        for k,v in ship_defaults.items():
            if k in blank_unit and blank_unit[k] == v:
                del blank_unit[k]
        
        min_data.update(blank_unit)
        
        # We already processed blank. Don't need it.
        variants.remove('blank')
        
        # Now we delete from units
        delete_ship_by_key(blank_unit[KEY], units)
        
        for variant in variants:
            # Get a copy of the variant
            var_unit = get_ship_by_name_and_variant(name, variant, units)
            if var_unit == None:
                print(f"{variant} not found for {name} in units")
                sys.exit(1)
                continue
            
            key = var_unit[KEY]

            # Remove defaults from blank
            for k,v in ship_defaults.items():
                if k in var_unit and var_unit[k] == v:
                    del var_unit[k]

            # Now we compare dictionary values against blank
            for k,v in blank_unit.items():
                if k in var_unit and var_unit[k] == v:
                    del var_unit[k]
            
            # We finally add the variant
            min_units.append({'data': var_unit})
            
            # Now we delete from units
            delete_ship_by_key(key, units)
        
            
    return min_root_object

       
# TODO - to be used when we remove upgrades stats from unit
def generate_cargo(unit, upgrades):
    key = unit['Key']
    cargo = []
    cargo_stats = {}
    
    if 'Cargo' in unit:
        cargo_split = unit['Cargo'].split('{')
        
        for c in cargo_split:
            if c == '':
                continue
        
            components = c.split(';')
            
            if len(components) == 0:
                continue
            
            cargo_key = components[0]
            if cargo_key == '':
                continue
            
            if cargo_key in upgrades:
                cargo_stats.update(upgrades[cargo_key])
    
    return cargo_stats
    
    
if __name__ == '__main__':
    # If run from Asset-Production, change to units folder
    if os.path.isdir('units'):
        path = os.getcwd()
        os.chdir(path + '/units')


    units = []
    base_template = {}
    
    with open('unit_template.json','r') as template_file:
        template_str = template_file.read()
        base_template = json.loads(template_str)
   
    
    with open('units_old.json', 'r') as units_file:
        units_str = units_file.read()
        units = json.loads(units_str)
    
    for key in delete_array:
        delete_ship_by_key(key, units)
    
    upgrades = generate_upgrades(units)
    minimize(units, upgrades, base_template)
    
    ships = group_ships(units)
    stacked_ships = stack_ships(units, ships)
    
    with open('units.json', 'w') as units_file:
        json.dump(units, units_file, ensure_ascii=False, indent=4)
        
    with open('ships.json', 'w') as units_file:
        json.dump(stacked_ships, units_file, ensure_ascii=False, indent=4)
        
    print("Success")
