import locale
import math
import json


newline = "#n#"
red = "#c1:.3:.3#"
green = "#c0:1:.5#"
light_grey = "#c.75:.9:1#"
grey = "#c.6:.7:.8#"
light_yellow = "#c.675:.925:.825#"
end_color = "#-c"

non_combat_speed_multiplier = 1
megajoules_multiplier = 1

with open('config.json', 'r') as file:
    data = json.load(file)
    non_combat_speed_multiplier = data['components']['drive']['non_combat_mode_multiplier']
    megajoules_multiplier = data['constants']['megajoules_multiplier']
    


# Format large number
def lnum(ship_stats, key, divider = 1.0):
    num = float(ship_stats[key])/divider
    num = '{:n}'.format(num)
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
    fl = float(ship_stats[key])/divider
    #s = f"{key} {fl}"
    #print(s)
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
    text += f"#-c{newline}{light_grey}Model: #-c{ship_stats['Name']}{light_grey}    {get_variant(ship_stats['Key'])}{newline}"
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
        if ship_stats[pair[1]] == '':
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
        
    return text


    
def get_ship_description(ship_stats):
    locale.setlocale(locale.LC_ALL, '')
    
    text = get_notes(ship_stats)
    text += get_general(ship_stats)
    text += get_flight(ship_stats)
    text += get_governor(ship_stats)
    text += get_radar(ship_stats)
    text += get_energy_spec_and_jump(ship_stats)
    text += get_durability(ship_stats)
                      
    return text

if __name__ == "__main__":
    # Test function
    # Useful to check python script for correctness before running VS
    
    with open('units/units.json', 'r') as file:
        data = json.load(file)
        
        for ship in data:
            if ship['Key'] == 'Llama.begin':
                t = get_ship_description(ship)
                t = t.replace('#n#','\n')
                print(t)
                break

    


