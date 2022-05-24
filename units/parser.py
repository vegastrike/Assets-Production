import random
import json
import sys

line_num = 0
column_num = 0

open_quotes = False
index = 0
column = 0
#headers = []
line_values = []
units = []
unit = {}

isKahan = False

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
    global open_quotes
    global index
    global line_values
    next_comma = line.find(",", index)
    next_quotes = line.find("\"", index)
    #print(f"comma:{next_comma} {next_quotes}")
    
    # We found neither
    if next_comma == -1 and next_quotes == -1:
        return -1
    
    if next_comma == -1:
        next_comma = next_quotes + 1
        
    elif next_quotes == -1:
        next_quotes = next_comma + 1
    
    if open_quotes:
        # We must have closed quotes 
        if next_quotes == -1:
            return -1
        
        open_quotes = False
        return next_quotes + 1
    
    if next_comma < next_quotes and next_comma != -1:
        return next_comma + 1
    
    open_quotes = True
    return next_quotes + 1



def parseNext(text, parse_headers = False):
    global index
    global line_num
    global line_values
    global column_num
    global max_columns
    
    global isKahan
    
    line_values = []
    previous_index = index
    index = next_in_line(text)
    
    if parse_headers:
        return
    
    if column_num == max_columns -1:
        key = headers[column_num] 
        value = text[previous_index:].strip()
        index = -1 
        if len(value) > 0:
            unit[key] = value
        else:
            unit[key] = ''
        
        #print("Error column_num is too big")
        #sys.exit()
        return
    
    key = headers[column_num] 
    value = text[previous_index:index-1].strip()
    
    if key == 'Key' and value == 'Kahan.blank':
        isKahan = True
    if key == 'Key' and value != 'Kahan.blank':
        isKahan = False
        
    if isKahan:
        print(f"{line_num} {index} {column_num} key={key} value={value}")
    
    if len(value) > 0:
        unit[key] = value
    else:
        unit[key] = ''
    #print(f"{line_num}:{index} {open_quotes} {value}")
    
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
            unit[headers[i]] = values[i]
        i += 1
        
    units.append(unit)


with open("units.csv", "r") as units_file:
    lines = units_file.readlines()
    for line in lines:
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
       
json_object = json.dumps(units, indent = 4)
with open("units.json", "w") as json_file:
    json_file.write(json_object)
print(json_object)
#print(json_object[523])
              
              
 
