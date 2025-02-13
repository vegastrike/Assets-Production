import json
import locale

locale.setlocale(locale.LC_ALL, '')  

def format_number(number) -> str:
    # large numbers - int with commas
    if number > 1000:
        int_number = '{:n}'.format(int(number))
        return str(int_number)
    
    # numbers that should be rounded


    return str(number)

def add_exceptions(unit, key):
    # Show Stats by default
    unit['Show_Stats'] = 'true'
    
    if 'passenger_quarters' in key:
        unit['Show_Stats'] = 'false'
    
    if 'shady' in key:
        return
    
    # Afterburner Upgrade
    if 'Afterburner_Accel' in unit:
        unit['Afterburner_Accel'] = int(float(unit['Afterburner_Accel']) * 100)
    if 'Afterburner_Speed_Governor' in unit:
        unit['Afterburner_Speed_Governor'] = int(float(unit['Afterburner_Speed_Governor']) * 100)
    if 'Afterburner_Usage_Cost' in unit:
        unit['Afterburner_Usage_Cost'] = int(float(unit['Afterburner_Usage_Cost']) * 100)

    # Basic Repair & Refuel
    if key == 'Basic Repair & Refuel':
        unit['description'] = '#c.75:.9:1#Hire starship mechanics to examine and assess any wear and tear on your craft. They will replace any damaged components on your vessel with the standard components of the vessel you initially purchased.  Further upgrades above and beyond the original will not be replaced free of charge.  The total assessment and repair cost applies if any components are damaged or need servicing (fuel, wear and tear on jump drive, etc...). If such components are damaged you may save money by repairing them on your own. Your vessel will also be refuelled.'
        unit['Show_Stats'] = 'false'

def process_shady(unit,key):
    if 'shady' not in key:
        return
    
    # Negative values - reduces by number
    negatives = {'Hold_Volume': 'Shady_Hold_Volume'}
    for original, shady in negatives.items():
        if original in unit and int(unit[original]) < 0:
            unit[shady] = -1 * int(unit[original])
            del unit[original]
    
    # Percentage
    percentages = {'Mass': 'Shady_Mass',
                   'Primary_Capacitor': 'Shady_Primary_Capacitor',
                   'Reactor_Recharge': 'Shady_Reactor_Recharge', 
                   'Hull': 'Shady_Hull', 
                   'Shield_Front_Top_Right': 'Shady_Shield_Front_Top_Right',
                   'Shield_Back_Top_Left': 'Shady_Shield_Back_Top_Left', # Dummy so won't print original
                   'Shield_Recharge': 'Shady_Shield_Recharge',
                   'Armor_Back_Top_Left': 'Shady_Armor_Back_Top_Left',
                   'Armor_Back_Bottom_Left': 'Shady_Armor_Back_Bottom_Left', # Dummy
                   'Afterburner_Accel': 'Shady_Afterburner_Accel',
                   'Forward_Accel': 'Shady_Forward_Accel', # Dummy
                   'Retro_Accel': 'Shady_Retro_Accel', # Dummy
                   'Maneuver_Yaw': 'Shady_Maneuver_Yaw',
                   'Maneuver_Pitch': 'Shady_Maneuver_Pitch', # Dummy
                   'Maneuver_Roll': 'Shady_Maneuver_Roll', # Dummy
                   'Yaw_Governor': 'Shady_Yaw_Governor', # Dummy
                   'Pitch_Governor': 'Shady_Pitch_Governor', # Dummy
                   'Roll_Governor': 'Shady_Roll_Governor'} # Dummy
        
    for original, shady in percentages.items():
        if original in unit:
            if float(unit[original]) > 1.0:
                unit[shady] = int(round(100* (float(unit[original])-1),0))
            else:
                unit[shady] = int(round(100* (1-float(unit[original])),0))
            del unit[original]
    
 

def get_shot_cycle_mul(upgrade):
    beam_weapon = upgrade['type'] == 'Beam'
    stability = upgrade['Energy.stability']
    refire = upgrade['Energy.refire']
    shot_cycle_mul= stability / (refire + stability) if beam_weapon else 1/refire
    return shot_cycle_mul

def process_weapon(upgrade, unit, vsdm):
    # Autotracking - need to remove superfluous weapon stats
    if unit['Name'] == 'Autotracking':
        unit['Name'] = 'Add Autotracking Capability'
        unit['Upgrade_Type'] = 'Autotrack'
        del unit['ammo_quantity']
        return
    
    # Mount capability - need to remove superfluous weapon stats
    if unit['Name'] == 'tractor_capability':
        unit['Name'] = 'Add Tractor Capability'
        unit['Upgrade_Type'] = 'Tractor_Capability'
        del unit['ammo_quantity']
        return
    
    # Non-lethal weapons - convert damage to positive and add text
    unit['nonlethal'] = ''
    if 'Damage.rate' in upgrade and upgrade['Damage.rate'] < 0:
        unit['nonlethal'] = '(non-lethal)'
        upgrade['Damage.rate'] = upgrade['Damage.rate'] * (-1)
    
    if 'Damage.phasedamage' in upgrade and upgrade['Damage.phasedamage'] < 0:
        unit['nonlethal'] = '(non-lethal)'
        upgrade['Damage.phasedamage'] = upgrade['Damage.phasedamage'] * (-1)
        
    unit.update(upgrade)
    
    # Extra stats at the bottom for continuous firing
    if 'Energy.refire' not in upgrade or 'Energy.stability' not in upgrade:
        return
    
    unit['Upgrade_Type'] = 'extra_weapon_stats'
    shot_cycle_mul = get_shot_cycle_mul(upgrade)
        
    if 'Damage.rate' in upgrade:
        unit['Damage.continuous_rate'] = round(upgrade['Damage.rate'] * shot_cycle_mul * vsdm,2)
    if 'Damage.phasedamage' in upgrade:
        unit['Damage.continuous_phasedamage'] = round(upgrade['Damage.phasedamage'] * shot_cycle_mul * vsdm,2)
    if 'Energy.rate' in upgrade:
        unit['Energy.continuous_rate'] = round(upgrade['Energy.rate'] * shot_cycle_mul * vsdm,2)
    
def process_resource(key, resource_text):
    exclude = ['description']
    if key in exclude:
        return resource_text
    
    print(f"{key} {resource_text}")
    parts = resource_text.split('/')

    damaged_index = 0
    original_index = 0

    if len(parts) == 2:
        damaged_index = 0
        original_index = 1
    elif len(parts) == 3:
        damaged_index = 1
        original_index = 2
    else:
        return resource_text
    
    damaged = float(parts[damaged_index])
    original = float(parts[original_index])

    return f"{format_number(damaged)} (orig: {format_number(original)})"
    
# We process a line to find the tag <key> or <key=value>
# <key> we convert to unit[key] and replace the tag with it.
# <key=value> we again convert and check if equal to value.
# This is used for text that is specific to certain upgrade types.
def process_line(line, unit):
    line = line.strip()
    if line == '':
        return ''
    
    if line.startswith('//'):
        # Comment
        return ''
    
    start_index = line.find('<')
    if start_index == -1:
        # Static line - just return it
        return line + "#n#" + '\n'
    
    end_index = line.find('>')
    if end_index == -1:
        # Something is wrong here
        return ''
    
    eq_index =  line.find('=')
    if eq_index == -1:
        key = line[start_index+1:end_index]

        if key in unit:
            value = process_resource(key, str(unit[key]))
            line = line[:start_index] + str(value) + line[end_index+1:]
            
            # Is there another tag?
            if line.find('<') != -1:
                return process_line(line, unit)
            
            return line + "#n#" + '\n'
        else:
            return '' 
    else:
        pair = line[start_index+1:end_index]
        key, value = pair.split('=')
        if key in unit and unit[key] == value:
            return line[end_index+1:] + "#n#" + '\n'
        
    return ''
   

def get_upgrade_info(unit_stats):
    key = unit_stats['upgrade_key']

    # Remove ship name - use upgrade name 
    if 'Name' in unit_stats:
        del unit_stats['Name']


    vsdm = 5.0
    with open('config.json', 'r') as file:
        data = json.load(file)
        vsdm = data['constants']['kj_per_unit_damage'] / data['constants']['kilo']
        
    unit = {}
    with open('units/units.json', 'r') as file:
        data = json.load(file)
        
        for upgrade in data:
            if upgrade['Key'] == key:
                unit.update(upgrade)
                break
    
    key = key.replace('__upgrades','')
    with open('master_component_list.json', 'r') as file:
        data = json.load(file)
        
        for upgrade in data:
            if upgrade['file'] == key:
                unit.update(upgrade)
                break
    
    # Process shield and armor
    if 'shield' in unit:
        shield_strength = unit['shield']
        unit['shield_front'] = shield_strength
        unit['shield_back'] = shield_strength
        unit['shield_left'] = shield_strength
        unit['shield_right'] = shield_strength
        del unit['shield']

    if 'armor' in unit:
        armor_strength = unit['armor']
        unit['armor_front'] = armor_strength
        unit['armor_back'] = armor_strength
        unit['armor_left'] = armor_strength
        unit['armor_right'] = armor_strength
        del unit['armor']

    # Process ammo and weapons
    if 'Mounts' in unit:
        mounts = unit['Mounts'][1:-1]
        mount_parts = mounts.split(';')
        key = mount_parts[0]
        unit['ammo_quantity'] = mount_parts[1]
    
    with open('weapons.json', 'r') as file:
        data = json.load(file)
        
        for upgrade in data:
            if upgrade['name'] == key:
                process_weapon(upgrade, unit, vsdm)
                
                break
    
    add_exceptions(unit, key)
    process_shady(unit,key)
    
    # Overwrite values in original upgrade with actual in ship (if relevant)
    for key in unit:
        if key in unit_stats:
            unit[key] = unit_stats[key]
            print(f"{key} {unit_stats[key]}")

    # Radar range in km not meters
    if 'Radar_Range' in unit:
        unit['Radar_Range'] = format_number(int(unit['Radar_Range'])/ 1000)

    text = ''
    
    with open('python/base_computer/upgrade_view.schema', 'r') as file:
        for line in file:
            text += process_line(line, unit)
    
    return text
    
    
if __name__ == "__main__":
    unit = {'Afterburner_Accel': '17000.00/17000.00/17000.00', 'Afterburner_Speed_Governor': '120.00/120.00/125.00', 'Bottom_Accel': '4000.00/4000.00/4000.00', 'Can_Cloak': '0', 'Can_Lock': '1', 'Cargo': '{armor02;upgrades/Armor;200.000000;1;20.000000;0.000000;1.000000;1.000000;;false;true}{capacitor02;upgrades/Capacitors/Standard;200.000000;1;4.000000;4.000000;1.000000;1.000000;;false;true}{reactor02;upgrades/Reactors/Standard;200.000000;1;2.000000;3.500000;1.000000;1.000000;;false;true}{add_spec_capacitor01;upgrades/SPEC_Capacitors;200.000000;1;5.000000;4.000000;1.000000;1.000000;;false;true}{skyscope1;upgrades/Sensors/Common;200.000000;1;0.010000;1.000000;1.000000;1.000000;;false;true}{quadshield02;upgrades/Shield_Systems/Standard_Quad_Shields;200.000000;1;2.000000;8.000000;1.000000;1.000000;;false;true}', 'Cargo_Import': '', 'Cloak_Energy': '0.000000', 'Cloak_Glass': '0', 'Cloak_Min': '0.000000', 'Cloak_Rate': '0.000000', 'Comm_Functionality': '1', 'Default_Speed_Governor': '120.00/120.00/125.00', 'ECM_Rating': '0', 'Equipment_Space': '0', 'FireControl_Functionality': '1', 'Forward_Accel': '17000.00/17000.00/17000.00', 'Fuel_Capacity': '25.00/25.00/25.00', 'Heat_Sink_Rating': '0', 'Hidden_Hold_Volume': '0', 'Hold_Volume': '2000', 'Hud_Functionality': '1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;', 'Hull': '500.00/500.00/500.00', 'ITTS': '1', 'Jump_Drive_Delay': '1.000000', 'Jump_Drive_Present': '0', 'Key': 'Llama.begin', 'Left_Accel': '4000.00/4000.00/4000.00', 'Lifesupport_Functionality': '1', 'Lock_Cone': '25', 'Maneuver_Pitch': '50000.00/50000.00/50000.00', 'Maneuver_Roll': '50000.00/50000.00/50000.00', 'Maneuver_Yaw': '50000.00/50000.00/50000.00', 'Mass': '250', 'Max_Comm_Functionality': '1', 'Max_Cone': '180', 'Max_FireControl_Functionality': '1', 'Max_Hud_Functionality': '1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;1;', 'Max_Lifesupport_Functionality': '1', 'Max_SPECDrive_Functionality': '1', 'Mounts': '{Laser;-1;15;LIGHT;7.084000;-0.476000;23.855999;0.000000;0.000000;0.000000;0.000000;1.000000;0.000000;1.000000;0.000000;1.000000;1.000000}{Laser;-1;15;LIGHT;-6.748000;-0.476000;23.855999;0.000000;0.000000;0.000000;0.000000;1.000000;0.000000;1.000000;0.000000;1.000000;1.000000}{Laser;-1;3;LIGHT;2.660000;1.232000;7.532000;0.000000;0.000000;0.000000;0.000000;1.000000;0.000000;1.000000;0.000000;1.000000;1.000000}{Laser;-1;3;LIGHT;-2.352000;1.232000;7.532000;0.000000;0.000000;0.000000;0.000000;1.000000;0.000000;1.000000;0.000000;1.000000;1.000000}{Dumbfire;48;48;LIGHT-MISSILE MEDIUM-MISSILE SPECIAL-MISSILE;0.000000;0.000000;0.000000;0.000000;0.000000;0.000000;0.000000;1.000000;0.000000;1.000000;0.000000;1.000000;1.000000}{;-1;48;LIGHT-MISSILE MEDIUM-MISSILE SPECIAL-MISSILE;0.000000;0.000000;0.000000;0.000000;0.000000;0.000000;0.000000;1.000000;0.000000;1.000000;0.000000;1.000000;1.000000}', 'Name': 'Llama', 'Outsystem_Jump_Cost': '200.000000', 'Pitch_Governor_Down': '50.00/50.00/50.00', 'Pitch_Governor_Up': '50.00/50.00/50.00', 'Primary_Capacitor': '0.33/0.33/0.33', 'Radar_Color': '0', 'Radar_Range': '3e+08', 'Reactor_Recharge': '44.000000', 'Repair_Droid': '0', 'Retro_Accel': '15000.00/15000.00/15000.00', 'Right_Accel': '4000.00/4000.00/4000.00', 'Roll_Governor_Left': '55.00/55.00/55.00', 'Roll_Governor_Right': '55.00/55.00/55.00', 'SPECDrive_Functionality': '1', 'Shield_Efficiency': '1', 'Shield_Leak': '0', 'Shield_Recharge': '8.00/8.00/8.00', 'Slide_End': '0', 'Slide_Start': '0', 'Spec_Interdiction': '0', 'Sub_Units': '', 'Textual_Description': "With Lauktk's death, ownership of this vessel has passed on to you.", 'Top_Accel': '4000.00/4000.00/4000.00', 'Tracking_Cone': '3.99998', 'Tractorability': 'p', 'Unit_Scale': '', 'Upgrade_Storage_Volume': '360', 'Upgrades': '', 'Warp_Capacitor': '0.67/0.67/0.67', 'Warp_Max_Multiplier': '1', 'Warp_Min_Multiplier': '1', 'Warp_Usage_Cost': '120.000000', 'Wormhole': '0', 'Yaw_Governor_Left': '45.00/45.00/45.00', 'Yaw_Governor_Right': '45.00/45.00/45.00', 'armor_back': '190.00/190.00/200.00', 'armor_front': '192.00/192.00/200.00', 'armor_left': '195.00/195.00/200.00', 'armor_right': '180.00/180.00/200.00', 'shield_back': '142.00/142.00/150.00', 'shield_facets': '4', 'shield_front': '138.00/138.00/150.00', 'shield_left': '145.00/145.00/150.00', 'shield_right': '150.00/150.00/150.00', 'upgrade_key': 'add_spec_capacitor01__upgrades'}
    unit['upgrade_key'] == 'skyscope1'
    t = get_upgrade_info(unit)
    #t = get_upgrade_info('Photon_MK_III_ammo__upgrades')
    #t = get_upgrade_info('Photon_MK_III__upgrades')
    #t = get_upgrade_info('armor01__upgrades')
    #t = get_upgrade_info('add_cargo_expansion__upgrades')
    #t = get_upgrade_info('ecm_package01__upgrades')
    #t = get_upgrade_info('cloaking_device__upgrades')
    #t = get_upgrade_info('jump_drive__upgrades')
    #t = get_upgrade_info('mult_overdrive01__upgrades')
    #t = get_upgrade_info(['upgrade_key': 'passenger_quarters_01__upgrades'])
    #t = get_upgrade_info('reactor09__upgrades')
    #t = get_upgrade_info('add_spec_capacitor01__upgrades')
    #t = get_upgrade_info('hawkeye2__upgrades')
    #t = get_upgrade_info('Micro_Driver__upgrades')
    #t = get_upgrade_info('Ktek_Mini_Grav-thumper__upgrades')
    #t = get_upgrade_info('autotracking__upgrades')
    #t = get_upgrade_info('Plasma_Plume__upgrades')
    #t = get_upgrade_info('tractor_capability__upgrades')
    #t = get_upgrade_info('Basic Repair & Refuel__upgrades')
    #t = get_upgrade_info('tractor_heavy__upgrades')
    #t = get_upgrade_info('mult_shady_moregunrecharge__upgrades')
    #t = get_upgrade_info('mult_shady_moreshields__upgrades')
    #t = get_upgrade_info('mult_shady_moreshieldrecharge__upgrades')
    #t = get_upgrade_info('mult_shady_moreupgrade__upgrades')
    #t = get_upgrade_info('mult_shady_morethrust__upgrades')
    
    print(t)

