import locale
import math
import json


newline = "#n#"
red = "#c1:.3:.3#"
green = "#c0:1:.5#"
light_grey = "#c.75:.9:1#"
grey = "#c.6:.7:.8#"
yellow = "#c.925:.925:.925#"
light_yellow = "#c.675:.925:.825#"
end_color = "#-c"

KEY = 'Key'
NAME = 'Name'
LC_NAME = 'name' # inconsistent. fix.
SUB_UNITS = 'Sub_Units'
MOUNTS = 'Mounts'

non_combat_speed_multiplier = 1
megajoules_multiplier = 1

with open('config.json', 'r') as file:
    data = json.load(file)
    non_combat_speed_multiplier = data['components']['drive']['non_combat_mode_multiplier']
    megajoules_multiplier = data['constants']['megajoules_multiplier']
    
# Wasteful
def get_unit(key):
    with open('units/units.json', 'r') as file:
        units = json.load(file)
        
        for unit in units:
            if unit[KEY] == key:
                return unit
            
        return None

# Format large number
def lnum(ship_stats, key, divider = 1.0) -> str:
    try:
        num = float(ship_stats[key])/divider
        num = '{:n}'.format(num)
    except KeyError:
        print('KeyError in lnum: ', key, ' not found in ship_stats')
        return ''
    except ZeroDivisionError:
        print('ZeroDivisionError in lnum')
        return ''
    except TypeError:
        print('TypeError in lnum')
        return ''
    except ValueError:
        print('ValueError in lnum')
        return ''
    return num

def get(ship_stats, key):
    return ship_stats[key]

def get_bool(ship_stats, key):
    s = ship_stats[key]
    if(s == 'TRUE' or s=='1'): 
        return True
    return False
    
def get_int(ship_stats, key):
    return int(ship_stats[key])

def get_dbl(ship_stats, key, divider = 1.0):
    try:
        fl = float(ship_stats[key])/divider
    except KeyError:
        print('KeyError in get_dbl: ', key, ' not found in ship_stats')
        return 0.0
    except ValueError:
        print('ValueError in get_dbl: ', ship_stats[key], ' could not be converted to a double')
        return 0.0
    except TypeError:
        print('TypeError in get_dbl')
        return 0.0

    return fl

def get_fmt_dbl(ship_stats, key, divider = 1.0):
    return "{:.2f}".format(float(ship_stats[key]))

def fmt_dbl(dbl):
    return "{:.2f}".format(dbl)

def near_equal(a,b):
    return a-b < 0.01 and b-a < 0.01

def get_notes(ship_stats):
    text = f"{green}[NOTES]{newline}{newline}"
    text += f"{grey}#-c{ship_stats['Textual_Description']}{newline}{newline}"
    return text

def get_variant(key):
    # TODO: refactor with dict and for/each
    if key.endswith('blank'):
        return ''
    if key.endswith('begin'):
        return 'Variant: #-cStock (Refurbished)'
    if key.endswith('stock'):
        return 'Variant: #-cStock'
    if key.endswith('civvie'):
        return 'Variant: #-cCivilian'
    if key.endswith('milspec'):
        return 'Variant: #-cMilspec'
    if key.endswith('rg'):
        return 'Variant: #-cRegional Guard'
    if key.endswith('rgspec'):
        return 'Variant: #-cRegional Guard Spec'
    
    return ''

def get_itts(itts):
    if(itts=='1'):
        return 'yes'
    return 'no'

def get_iff(iff):
    if iff=='0': return 'none'
    if iff=='1': return 'friend/foe'
    if iff=='2': return 'object recognition'
    return iff

# General
def get_general(ship_stats):
    text = f"{green}[GENERAL INFORMATION]{newline}"
    text += f"#-c{newline}{light_grey}Model: #-c{ship_stats['Name']}{light_grey}    {get_variant(ship_stats[KEY])}{newline}"
    text += f"{light_grey}Mass: #-c{lnum(ship_stats,'Mass')} metric tons{newline}"
    text += f"{light_grey}Hold volume: #-c{lnum(ship_stats,'Hold_Volume')} cubic meters{newline}"
    text += f"{light_grey}Upgrade volume: #-c{lnum(ship_stats,'Upgrade_Storage_Volume')} cubic meters{newline}"
    text += f"{light_grey}Fuel capacity: #-c{lnum(ship_stats,'Fuel_Capacity')} metric tons of Lithium-6{newline}{newline}"
    return text

# Flight Characteristics
def get_flight(ship_stats):
    mass = get_dbl(ship_stats,'Mass')
    divider = 9.8 * mass
    divider_maneuver = mass * 180 / math.pi
    yaw = get_dbl(ship_stats,'Maneuver_Yaw', divider_maneuver)
    pitch = get_dbl(ship_stats,'Maneuver_Pitch', divider_maneuver)
    roll = get_dbl(ship_stats,'Maneuver_Roll', divider_maneuver)
    
    forward = get_dbl(ship_stats,'Forward_Accel', divider)
    retro = get_dbl(ship_stats,'Retro_Accel', divider)
    
    lateral = (get_dbl(ship_stats,'Left_Accel', divider) + get_dbl(ship_stats,'Right_Accel', divider))/2
    vertical = (get_dbl(ship_stats,'Top_Accel', divider) + get_dbl(ship_stats,'Bottom_Accel', divider))/2
    
    afterburner = get_dbl(ship_stats,'Afterburner_Accel', divider)
    
    text = f"{green}[FLIGHT CHARACTERISTICS]{newline}"
    
    if(yaw == pitch and yaw == roll):
        text += f"#-c{newline}{light_grey}Turning response: #-c{fmt_dbl(yaw)} radians/second²{newline}"
        text += f"{grey}  (yaw, pitch, roll)#-c{newline}"
    else:
        text += f"#-c{newline}{light_grey}  yaw #-c{fmt_dbl(yaw)} radians/second²{newline}"
        text += f"#-c{newline}{light_grey}  pitch #-c{fmt_dbl(pitch)} radians/second²{newline}"
        text += f"#-c{newline}{light_grey}  roll #-c{fmt_dbl(roll)} radians/second²{newline}"
    
    text += f"{light_grey}Fore acceleration: #-c{fmt_dbl(forward)} gravities{newline}"
    text += f"{light_grey}Aft acceleration: #-c{fmt_dbl(retro)} gravities{newline}"
    
    if(lateral == vertical):
        text += f"{light_grey}Orthogonal acceleration: #-c{fmt_dbl(lateral)} gravities{newline}"
        text += f"{grey}(vertical and lateral axes)#-c{newline}"
    else:
        text += f"{light_grey} Lateral acceleration #-c{fmt_dbl(lateral)} gravities{newline}"
        text += f"{grey} Vertical acceleration #-c{fmt_dbl(vertical)} gravities{newline}"
    text += f"{light_grey}Forward acceleration with overthrust: #-c{fmt_dbl(afterburner)} gravities{newline}{newline}"
    return text

def get_governor(ship_stats):
    divider = 180 / math.pi
    speed = get_int(ship_stats, 'Default_Speed_Governor')
    afterburner = get_int(ship_stats, 'Afterburner_Speed_Governor')
    
    yaw = get_dbl(ship_stats, 'Yaw_Governor',divider)
    #yaw_right = get_dbl(ship_stats, 'Yaw_Governor_Right')
    #yaw_left = get_dbl(ship_stats, 'Yaw_Governor_Left')
    
    pitch = get_dbl(ship_stats, 'Pitch_Governor',divider)
    #pitch_down = get_dbl(ship_stats, 'Pitch_Governor_Up')
    #pitch_up = get_dbl(ship_stats, 'Pitch_Governor_Down')
    
    roll = get_dbl(ship_stats, 'Roll_Governor',divider)
    #roll_right = get_dbl(ship_stats, 'Roll_Governor_Right')
    #roll_left = get_dbl(ship_stats, 'Roll_Governor_Left')
    
    text = f"{green}[GOVERNOR SETTINGS]{newline}#-c{newline}"
    text += f"{light_grey}Max combat speed: #-c{speed} m/s{newline}"
    text += f"{light_grey}Max overdrive combat speed: #-c{afterburner} m/s{newline}"
    text += f"{light_grey}Max non-combat speed: #-c{speed * non_combat_speed_multiplier} m/s{newline}"
    text += f"{light_grey}Max turn rates:#-c{newline}"
    text += f"{light_yellow} - yaw: #-c{fmt_dbl(yaw)} radians/second{newline}"
    text += f"{light_yellow} - pitch: #-c{fmt_dbl(pitch)} radians/second{newline}"
    text += f"{light_yellow} - roll: #-c{fmt_dbl(roll)} radians/second{newline}{newline}"
    return text

def get_radar(ship_stats):
    radar_range = lnum(ship_stats,'Radar_Range',1000)
    max_cone = get_dbl(ship_stats,'Max_Cone', 180 / math.pi) 
    tracking_cone = get_dbl(ship_stats,'Tracking_Cone', 180 / math.pi)
    lock_cone = get_dbl(ship_stats,'Lock_Cone', 180 / math.pi)
    itts = ship_stats['ITTS']
    iff = ship_stats['Radar_Color']
    
    text = f"{green}[TARGETTING SUBSYSTEM]{newline}#-c{newline}"
    text += f"{light_grey}Tracking range: #-c{radar_range} km{newline}"
    
    if(near_equal(max_cone,math.pi)):
        text += f"{light_grey}Tracking cone: #-cOmni-directional{newline}"
    else:
        text += f"{light_grey}Tracking cone: #-c{fmt_dbl(max_cone * 2)} radians{newline}"
        text += f"{light_grey} (planar angle: 2 pi means full space)#-c{newline}"
    text += f"{light_grey}Assisted targeting cone: #-c{fmt_dbl(tracking_cone * 2)} radians{newline}"
    text += f"{light_grey}Missile locking cone: #-c{fmt_dbl(lock_cone * 2)} radians{newline}"
    text += f"{light_grey}ITTS (Intelligent Target Tracking System) support: #-c{get_itts(itts)}{newline}"
    text += f"{light_grey}AFHH (Advanced Flag & Hostility Heuristics) support: #-c{get_iff(iff)} {newline}{newline}"
    return text

def get_energy_spec_and_jump(ship_stats):
    reactor = get_dbl(ship_stats,'Reactor_Recharge',1/megajoules_multiplier)
    energy = get_dbl(ship_stats,'Primary_Capacitor',1/megajoules_multiplier)
    ftl_energy = get_dbl(ship_stats,'Warp_Capacitor',1/megajoules_multiplier)
    spec_cost = get_dbl(ship_stats,'Warp_Usage_Cost',1/megajoules_multiplier)

    jump_drive_installed = get_bool(ship_stats,'Jump_Drive_Present')
    jump_delay = get_dbl(ship_stats,'Jump_Drive_Delay')
    jump_cost = get_dbl(ship_stats,'Outsystem_Jump_Cost',1/megajoules_multiplier)


    text = f"{green}[ENERGY SUBSYSTEM]{newline}#-c{newline}"
    text += f"{light_grey}Recharge: #-c{reactor} MJ/s{newline}"
    text += f"{light_grey}Main capacitor: #-c{energy} MJ{newline}"
    text += f"{light_grey}SPEC capacitor: #-c{ftl_energy}0 MJ{newline}{newline}"
    
    text += f"{green}[SPEC SUBSYSTEM]{newline}#-c{newline}"
    text += f"{light_grey}Active SPEC Energy Requirements: #-c{spec_cost} MJ/s{newline}{newline}"
    
    text += f"{green}[JUMP SUBSYSTEM]{newline}#-c{newline}"
    if(jump_drive_installed):
        text += f"{light_grey}Energy cost for jumpnode travel: #-c{jump_cost} MJ{newline}"
        text += f"{light_grey}Delay: #-c{jump_delay} seconds{newline}{newline}"
    else:  
        text += f"{red}No outsystem jump drive present{end_color}{newline}{newline}"
        
    return text
  
def get_durability(ship_stats):
    armor = [
        ('Fore-starboard-high','Armor_Front_Top_Right'),
        ('Aft-starboard-high','Armor_Back_Top_Right'),
        ('Fore-port-high','Armor_Front_Top_Left'),
        ('Aft-port-high','Armor_Back_Top_Left'),
        ('Fore-starboard-low','Armor_Front_Bottom_Right'),
        ('Aft-starboard-low','Armor_Back_Bottom_Right'),
        ('Fore-port-low','Armor_Front_Bottom_Left'),
        ('Aft-port-low','Armor_Back_Bottom_Left'),
    ]
    
    shield4 = [
        ('Port','Shield_Front_Bottom_Left'),('Starboard','Shield_Front_Bottom_Right'),('Fore','Shield_Front_Top_Right'),('Aft','Shield_Back_Top_Left'),
    ]
    
    shield2 = [
        ('Fore','Shield_Front_Top_Right'),('Aft','Shield_Back_Top_Left'),
    ]
    
    # This is a kludge. Should go away when we refactor units.json and unit_csv.cpp
    shield_stat = {}
    num_emitters = 0
    for pair in shield4:
        if not pair[1] in ship_stats:
            continue
        value = get_dbl(ship_stats,pair[1])
        if value > 0:
            num_emitters += 1
    
            
    hull = lnum(ship_stats,'Hull')
    shield_recharge = lnum(ship_stats,'Shield_Recharge')
    
    text = f"{green}[DURABILITY STATISTICS]{newline}#-c{newline}"
    text += f"{light_grey}Sustainable Hull Damage: #-c{hull} MJ{newline}{newline}"
    
    text += f"{light_grey}Armor#-c{newline}"
    for pair in armor:
        armor_stat = lnum(ship_stats, pair[1])
        text += f"{light_yellow} - {pair[0]}: #-c{armor_stat} MJ{newline}"
    
    text += f"{newline}{light_grey}Shields#-c{newline}"
    text += f"{light_grey}Shield recharge: #-c{shield_recharge} MJ/s{newline}"
    if num_emitters == 0:
        text += f"{red}No shielding.{end_color}{newline}{newline}"
    elif num_emitters == 2:
        text += f"{light_grey}Number of shield emitter: 2{end_color}{newline}"
        for pair in shield2:
            shield_stat = lnum(ship_stats, pair[1])
            text += f"{light_yellow} - {pair[0]}: #-c{shield_stat} MJ{newline}"
    else:
        text += f"{light_grey}Number of shield emitter: 4{end_color}{newline}"
        for pair in shield4:
            shield_stat = lnum(ship_stats, pair[1])
            text += f"{light_yellow} - {pair[0]}: #-c{shield_stat} MJ{newline}"
    
    if 'Can_Cloak' in ship_stats and ship_stats['Can_Cloak'] == '1':
        text += f"{light_grey}Cloaking device installed.{end_color}{newline}"
    text += f"{newline}"
    return text

# this gets a list of subunits as a dictionary of turret type/number of type
# e.g. {'turret_flaq', 3}
def get_sub_units_summary(ship_stats):
    sub_units = {}
    
    if SUB_UNITS not in ship_stats:
        return sub_units
    
    sub_units_str = ship_stats[SUB_UNITS]
    sub_units_str_components = sub_units_str.split('{')
    
    for component in sub_units_str_components:
        semi = component.find(';')
        if semi == -1:
            continue
        sub_unit = component[0:semi]
        
        if sub_unit in sub_units:
            sub_units[sub_unit] += 1
        else:
            sub_units[sub_unit] = 1
    
    return sub_units

# Same as above
def get_mounts_summary(ship_stats):
    if MOUNTS not in ship_stats:
        return {}
    
    mounts_str = ship_stats[MOUNTS]
    
    mounts = {}
    
    primary_components = mounts_str.split('{')
    
    for primary_component in primary_components:
        secondary_components = primary_component.split(';')
        
        if len(secondary_components) < 6:
            continue
        
        mount = (secondary_components[0], secondary_components[3])
        
        if mount not in mounts:
            mounts[mount] = 1
        else:
            mounts[mount] += 1
        
    
    return mounts


def get_weapon_from_json(name):
    with open('weapons.json', 'r') as file:
        data = json.load(file)
        
        for weapon in data:
            if LC_NAME in weapon and weapon[LC_NAME] == name:
                return weapon
            
    return None

def get_weapon_details(weapon, vsdm, remaining = ''):
    # Non-lethal weapons - convert damage to positive and add text
    text = '' 
    
    if 'Damage.rate' in weapon:
        damage = weapon['Damage.rate']
        
        if damage  < 0:
            text += f"{light_grey}  - Damage: {damage * vsdm}MJ (non-lethal){end_color}{newline}"
        else:
            text += f"{light_grey}  - Damage: {damage * vsdm}MJ {end_color}{newline}"
    
    if 'Damage.phasedamage' in weapon:
        damage = weapon['Damage.phasedamage']
        
        if damage  < 0:
            text += f"{light_grey}  - Phase Damage: {damage * vsdm}MJ (non-lethal){end_color}{newline}"
        else:
            text += f"{light_grey}  - Phase Damage: {damage * vsdm}MJ {end_color}{newline}"
    
    if 'Energy.rate' in weapon and weapon['Energy.rate'] > 0:
        energy = weapon['Energy.rate']
        text += f"{light_grey}  - Energy: {energy}{end_color}{newline}"
        
    if 'Energy.refire' in weapon:
        refire = weapon['Energy.refire']
        text += f"{light_grey}  - Fires every: {refire} seconds{end_color}{newline}"
        
    if 'Distance.range' in weapon:
        range_ = weapon['Distance.range']
        text += f"{light_grey}  - Range: {range_}{end_color}{newline}"
    
    if 'Energy.locktime' in weapon:
        lock = weapon['Energy.locktime']
        text += f"{light_grey}  - Time to lock: {lock} seconds{end_color}{newline}"
        
        if remaining != '':
            text += f"{light_grey}  - Missiles remaining: {remaining}{end_color}{newline}"
        
        
    return text
    

def get_mounts(ship_stats):
    if MOUNTS not in ship_stats:
        return []
    
    mounts_str = ship_stats[MOUNTS]
    
    mounts = []
    
    primary_components = mounts_str.split('{')
    
    for primary_component in primary_components:
        secondary_components = primary_component.split(';')
        
        if len(secondary_components) < 6:
            continue
        
        mounts.append((secondary_components[0], secondary_components[3], secondary_components[1]))
    
    return mounts

def get_weapons(ship_stats):
    text = f"{green}[ARMAMENTS]{newline}#-c{newline}"
    text += f"{green}MOUNT POINTS{newline}#-c{newline}"
    
    # Print mount points summary
    mp_summary = get_mounts_summary(ship_stats)
    for mount,quantity in mp_summary.items():
        if quantity == 1:
            text += f"{light_grey}1 mount point of type {green}{mount[0]} {light_yellow}{mount[1]}{end_color}{newline}"
        else:
            text += f"{green}{quantity}{light_grey} mount points of type {green}{mount[0]} {light_yellow}{mount[1]}{end_color}{newline}"
    
    # TODO: print each weapon info once
    mounts = get_mounts(ship_stats)
    for mount in mounts:
        text += f"{light_grey}{mount[0]} {yellow}{mount[1]}{end_color}{newline}"
        
        if len(mount[0]) > 0:
            # Weapon installed
            weapon = get_weapon_from_json(mount[0])
            
            if weapon != None:
                text += get_weapon_details(weapon, 5400, mount[2])
                continue
            
            # Can't find weapon. It's a missile
            ammo_dummy_unit = get_unit(mount[0] + '_ammo__upgrades')
            if ammo_dummy_unit == None:
                continue # Couldn't find missile unit
            
            ammo_dummy_mounts = get_mounts(ammo_dummy_unit)
            weapon = get_weapon_from_json(ammo_dummy_mounts[0][0])
            
            if weapon != None:
                text += get_weapon_details(weapon, 5400, mount[2])
            
            
        
    return text
        

# This is a recursive function, as some turrets have turrets
# I didn't check but there may be edge cases where a turret has two turrets or some 
# nonsense like that. If it does, it won't be printed correctly.

# Also, if there's a loop, e.g. turret pointing to itself, we'll loop infinitely.
def get_turret_gun(turret_stats, level = 0):
    text = ''
    
    if level == 5:
        return text
    
    if SUB_UNITS in turret_stats:
        sub_units = get_sub_units_summary(turret_stats)
        
        for key in sub_units:
            sub_unit = get_unit(key)
            
            if key == None:
                continue
            
            gun = get_turret_gun(sub_unit, level +1)
            if gun != None:
                text += gun
    
    # We're processing the ship itself
    if level == 0:
        return text
    
    
    mounts = get_mounts(turret_stats)
        
    for mount in mounts:
        text += f"{light_grey}{mount[0]} {mount[1]}{end_color}{newline}"
        weapon = get_weapon_from_json(mount[0])
        if weapon != None:
            text += get_weapon_details(weapon, 5400)
    return text


# This returns the text
def get_turrets(ship_stats):
    sub_units = get_sub_units_summary(ship_stats)
    
    if len(sub_units) == 0:
        return ''
    
    text = f"{green}[SUB-UNITS]{newline}#-c{newline}"
    
    for key, quantity in sub_units.items():
        sub_unit = get_unit(key)
        
        if sub_unit == None:
            continue
        
        # Really shouldn't happen
        if quantity <= 0:
            continue
        
        if quantity == 1:
            text += f"{light_grey}1 turret of type {sub_unit['Name']}{end_color}{newline}"
        
        else:
            text += f"{light_grey}{quantity} turrets of type {sub_unit['Name']}{end_color}{newline}"
        
        gun = get_turret_gun(ship_stats, 0)
        
        if gun != None:
            text += gun
    
    return text

 
def clean_ship_stats(ship_stats):
    skip = ['Directory']
    for key, value in ship_stats.items():
        resource: list[str] = value.split('/')
        
        # Check if resource
        if len(resource) != 3:
            continue
        
        # Skip?
        if key in skip:
            continue

        try:
            ship_stats[key] = float(resource[0])
        except ValueError:
            continue


def get_ship_description(ship_stats):
    clean_ship_stats(ship_stats)
    locale.setlocale(locale.LC_ALL, '')
    
    text = get_notes(ship_stats)
    text += get_general(ship_stats)
    text += get_flight(ship_stats)
    text += get_governor(ship_stats)
    text += get_radar(ship_stats)
    text += get_energy_spec_and_jump(ship_stats)
    text += get_durability(ship_stats)
    text += get_weapons(ship_stats)
    text += get_turrets(ship_stats)
                      
    return text

if __name__ == "__main__":
    # Test function
    # Useful to check python script for correctness before running VS
    
    with open('units/units_old.json', 'r') as file:
        data = json.load(file)
        
        for ship in data:
            if ship[KEY] == 'Vigilance':
                t = get_ship_description(ship)
                t = t.replace('#n#','\n')
                print(t)
                
                break
