import random
import json

line_num = 0
column_num = 0
max_columns = 0
open_quotes = False
index = 0
column = 0
headers = []
line_values = []
units = []
unit = {}

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
    
    line_values = []
    previous_index = index
    index = next_in_line(text)
    
    if parse_headers:
        return
    
    if column_num >= max_columns:
        return
    
    key = headers[column_num] 
    value = text[previous_index:index-1].strip()
    
    if len(value) > 0:
        unit[key] = value
    #print(f"{line_num}:{index} {open_quotes} {value}")
    
def parseLine(text):
    global index
    global column_num
    global unit
    global units
    
    column_num = 0
    index = 0
    unit = {}
    
    while index != -1:
        parseNext(text)
        column_num +=1
        
    units.append(unit)

def addHeaders(text):
    global headers
    
    if text == ",":
        return
    
    if text.endswith(","):
        length = len(text)
        headers.append(text[0:length-1])

def generateHeaders(text):
    global index
    global headers
    global max_columns
    
    index = 0
    while index != -1:
        old_index = index
        parseNext(text, True)
        addHeaders(text[old_index:index])
    addHeaders(text[old_index:])
    headers[0] = "Key"
    max_columns = len(headers)

with open("units.csv", "r") as units_file:
    lines = units_file.readlines()
    for line in lines:
        if line_num == 0:
            generateHeaders(line)
            first_line = False

        elif line_num == 1:
            pass
        else:
            print("parsing line 2")
            
            parseLine(line)
            #break
        
        line_num +=1
       
json_object = json.dumps(units, indent = 4)
with open("units.json", "w") as json_file:
    json_file.write(json_object)
print(json_object)
              
              
