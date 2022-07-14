import json
import sys

master_array = []

def main():
    with open("../master_part_list_2.csv", "r") as parts_file:
        lines = parts_file.readlines()
        first_line = True
        for line in lines:
            if first_line:
                first_line = False
                continue
            line = line.rstrip('\n')
            parseLine(line)

    json_object = json.dumps(master_array, indent = 4)
    print(json_object)
    with open("../master_part_list.json", "w") as json_file:
        json_file.write(json_object)


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

    master_array.append(dictionary)
    
# by default execute `main()` when loaded as a script
if __name__ == "__main__":
   sys.exit(main())
