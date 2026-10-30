# Convert all csv files in .vegastrike to json

import json
import csv
from os import listdir
from os.path import isfile, join


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


     

def list_folders_or_files(folder, list_files = True):
    file_list = []
    #dirs = [f for f in listdir(folder) if not isfile(join(folder, f))]
    for f in listdir(folder):
        file_path = join(folder, f)

        if list_files and isfile(file_path):
            file_list.append(file_path)
        if not list_files and not isfile(file_path):
            file_list.append(file_path)

    return file_list
   
              
 # TODO: argparse and the like
# For now, run this from inside serialized_xml
if __name__ == "__main__":
    save_folder = '.'
    save_folders = list_folders_or_files(save_folder, False)
    for folder in save_folders:
        files = list_folders_or_files(folder)
        for file in files:
            headers = []
            content = []
            firstline = True

            if not file.endswith('.csv'):
                continue

            with open(file) as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                for row in csvreader:
                    # print(row)
                    for column in row:
                        if firstline:
                            headers.append(column)
                        else:
                            content.append(column) 

                    firstline = False

            dict = {}
            for h,c in zip(headers, content):
                dict[h] = c

            # game expects a list of ships
            # TODO: make it happen. We don't need one file per ship
            array = [dict]
            
            json_file_name = file.replace('.csv', '.json')
            with open(json_file_name, 'w') as json_file: 
                json.dump(array, json_file, ensure_ascii=False, indent=4)