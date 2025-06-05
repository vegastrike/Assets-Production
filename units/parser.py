# Convert unit.csv to unit.json

import random
import json
import sys

line_num = 0
column_num = 0

index = 0
column = 0
line_values = []
units = []
unit = {}


headers = ["Key", "Directory",	"Name",	"STATUS",	"Object_Type",
                            "Combat_Role",	"Textual_Description",	"Hud_image",	"Unit_Scale",	"Cockpit",
                            "CockpitX", "CockpitY",	"CockpitZ",	"Mesh",	"Shield_Mesh",	"Rapid_Mesh",	"BSP_Mesh",
                            "Use_BSP", "Use_Rapid",	"NoDamageParticles", "Mass",	"Moment_Of_Inertia",
                            "Fuel_Capacity",	"Hull", "Armor_Front_Top_Right",	"Armor_Front_Top_Left",
                            "Armor_Front_Bottom_Right", "Armor_Front_Bottom_Left",	"Armor_Back_Top_Right",
                            "Armor_Back_Top_Left", "Armor_Back_Bottom_Right",	"Armor_Back_Bottom_Left",	"Shield_Front_Top_Right",
                            "Shield_Back_Top_Left",	"Shield_Front_Bottom_Right",	"Shield_Front_Bottom_Left",
                            "Shield_Back_Top_Right",	"Shield_Front_Top_Left",	"Shield_Back_Bottom_Right",
                            "Shield_Back_Bottom_Left",	"Shield_Recharge",	"Shield_Leak",	"Warp_Capacitor",
                            "Primary_Capacitor",	"Reactor_Recharge",	"Jump_Drive_Present",	"Jump_Drive_Delay",
                            "Wormhole",	"Outsystem_Jump_Cost",	"Warp_Usage_Cost",	"Afterburner_Type",
                            "Afterburner_Usage_Cost",	"Maneuver_Yaw",	"Maneuver_Pitch",	"Maneuver_Roll",
                            "Yaw_Governor",	"Pitch_Governor",	"Roll_Governor",	"Afterburner_Accel",
                            "Forward_Accel",	"Retro_Accel",	"Left_Accel",	"Right_Accel",	"Top_Accel",
                            "Bottom_Accel",	"Afterburner_Speed_Governor",	"Default_Speed_Governor",	"ITTS",
                            "Radar_Color",	"Radar_Range",	"Tracking_Cone",	"Max_Cone", "Lock_Cone",	"Hold_Volume",
                            "Can_Cloak",	"Cloak_Min",	"Cloak_Rate",	"Cloak_Energy",	"Cloak_Glass",	"Repair_Droid",
                            "ECM_Rating",	"ECM_Resist",	"Ecm_Drain",	"Hud_Functionality",	"Max_Hud_Functionality",
                            "Lifesupport_Functionality",	"Max_Lifesupport_Functionality",	"Comm_Functionality",
                            "Max_Comm_Functionality",	"FireControl_Functionality",	"Max_FireControl_Functionality",
                            "SPECDrive_Functionality",	"Max_SPECDrive_Functionality",	"Slide_Start",	"Slide_End",
                            "Activation_Accel",	"Activation_Speed",	"Upgrades", "Prohibited_Upgrades",
                            "Sub_Units", "Sound", "Light", "Mounts", "Net_Comm", "Dock", "Cargo_Import",	"Cargo",
                            "Explosion", "Num_Animation_Stages", "Upgrade_Storage_Volume",	"Heat_Sink_Rating",
                            "Shield_Efficiency", "Num_Chunks", "Chunk_0", "Collide_Subunits",	"Spec_Interdiction", "Tractorability"]
max_columns = len(headers)
print(headers)

def next_in_line(text):
    global index
    global line_values
    next_comma = line.find(",", index)
    
    # We found neither
    if next_comma == -1:
        return -1
    
    return next_comma + 1

    
def parseLine(text):
    global index
    global column_num
    global unit
    global units
    
    column_num = 0
    index = 0
    unit = {}
    
    values = text.split(',')
    
    i = 0
    
    while i < max_columns :
        if len(values[i]) > 0:
            values[i] = values[i].replace("|", ",")
            unit[headers[i]] = values[i]
        i += 1
        
    units.append(unit)


with open("units.csv", "r") as units_file:
    lines = units_file.readlines()
    for line in lines:
        line = line.replace('"', '')
        if line_num == 0:
            pass
        elif line_num == 1:
            pass
        elif line_num == 2:
            pass
        elif line_num == len(lines) - 1:
            pass
        else:
            line = line.strip()
            parseLine(line)
        
        line_num +=1
     
# Merge unit_description
with open("units_description.csv") as description_file:
    lines = description_file.readlines()
    for line in lines:
        descriptions = line.split(',',1)
        if len(descriptions)<2:
            continue
        
        found = False
        for unit in units:
            if unit['Key'].lower() == descriptions[0].lower():
                unit['Textual_Description'] = descriptions[1]
                found = True
                print(f"Found {descriptions[0]}. Merged.")
                break
        
        if not found:
            unit = {'Key': descriptions[0], 'Textual_Description': descriptions[1]}
            units.append(unit)
            print(f"Not found {descriptions[0]}. Adding...")
     
     
json_object = json.dumps(units, indent = 4)
with open("units_old.json", "w") as json_file:
    json_file.write(json_object)
#print(json_object)
              
              
 
