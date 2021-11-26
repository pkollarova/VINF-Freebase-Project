from array import array
import io
import os
import re
import json
import sys
import os.path
import time

if sys.version_info[0] >= 3:
    unicode = str

current_id = None
name_list = list()
current_relation = None
names = ""

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
for read_line in input_stream:
#for read_line in sys.stdin:
    read_line = read_line.strip()
    splitted_line = read_line.split("\t")
    left_col = splitted_line[0]
    center_col = splitted_line[1]
    right_col = ""
    
    if center_col == "an_artist":
        current_id = left_col
        current_relation = None
        print(left_col + "\tan_artist")
        continue

    if current_id == None and current_relation == None:
        name_list = list()
        names = ""
        continue

    if current_id == left_col:
        if current_relation == None:
            name_list = list()
            names = ""
            current_relation = center_col
        if current_relation == center_col:
            if splitted_line[2] not in name_list:
                name_list.append(splitted_line[2])
                names += splitted_line[2] + " ~~~ "
            continue
        else:
            if current_id == None:
                current_relation = None
                name_list = list()
                names = ""
                continue
            #print(names)
            print(str(current_id) + "\t" + str(current_relation) + "\t" + " ~~~ ".join(name_list))
            current_relation = center_col
            name_list = list()
            names = ""
            name_list.append(splitted_line[2])
            names += splitted_line[2] + " ~~~ "
            continue
    else:
        if center_col == "an_artist":
            current_id = left_col
            print(left_col + "\tan_artist")
            current_relation = None
            name_list = list()
            names = ""
            continue
        else:
            if len(name_list) > 0:
                #print(names)
                print(str(current_id) + "\t" + str(current_relation) + "\t" + " ~~~ ".join(name_list))
            current_id = None
            current_relation = None
            name_list = list()
            names = ""
            
