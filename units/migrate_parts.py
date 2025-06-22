import json
import sys



def main():
    master_array = []
    
    with open("../master_part_list_2.csv", "r") as parts_file:
        lines = parts_file.readlines()
        first_line = True
        for line in lines:
            if first_line:
                first_line = False
                continue
            line = line.rstrip('\n')
            master_array.append(parseLine(line))

    with open("../master_part_list.json", "w") as json_file:
        json.dump(master_array, json_file, indent=4)


def parseLine(line):
    keys = ('file','categoryname','price','mass','volume',	'description')
    
    values = line.split(',')
    dictionary = {}
    i = 0
    
    key = values[0]
    if len(key) == 0:
        return
    
    for value in values:
        value = value.replace("~", ",")
        dictionary[keys[i]] = value
        i = i + 1

    return dictionary
    
    
# by default execute `main()` when loaded as a script
if __name__ == "__main__":
   sys.exit(main())
