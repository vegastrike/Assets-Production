import json        
        

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
            line = line[:start_index] + str(unit[key]) + line[end_index+1:]
            
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
   

def get_upgrade_info(key):
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
    if 'shield_strength' in unit:
        shield_strength = unit['shield_strength']
        unit['shield_front'] = shield_strength
        unit['shield_back'] = shield_strength
        unit['shield_left'] = shield_strength
        unit['shield_right'] = shield_strength
        del unit['shield_strength']

    if 'armor_strength' in unit:
        armor_strength = unit['armor_strength']
        unit['armor_front'] = armor_strength
        unit['armor_back'] = armor_strength
        unit['armor_left'] = armor_strength
        unit['armor_right'] = armor_strength
        del unit['armor_strength']


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
        
    text = ''
    
    with open('python/base_computer/upgrade_view.schema', 'r') as file:
        for line in file:
            text += process_line(line, unit)
    
    return text
    
    
if __name__ == "__main__":
    #t = get_upgrade_info('Photon_MK_III_ammo__upgrades')
    #t = get_upgrade_info('Photon_MK_III__upgrades')
    #t = get_upgrade_info('armor01__upgrades')
    #t = get_upgrade_info('add_cargo_expansion__upgrades')
    #t = get_upgrade_info('ecm_package01__upgrades')
    #t = get_upgrade_info('cloaking_device__upgrades')
    #t = get_upgrade_info('jump_drive__upgrades')
    #t = get_upgrade_info('mult_overdrive01__upgrades')
    t = get_upgrade_info('passenger_quarters_01__upgrades')
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

