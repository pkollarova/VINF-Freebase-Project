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
data_list = list()
dic = {} 
dic[0] = None
dic[1] = None
dic[2] = None
finala = ""

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


for read_line in input_stream:
#for read_line in sys.stdin:
    read_line = read_line.strip()
    splitted_line = read_line.split("\t")
    left_col = splitted_line[0]
    center_col = splitted_line[1]
    right_col = splitted_line[2]

    if str(current_id) == "None":
        if len(dic) > 0:
            finala = str(dic[0]) + " ***** " + str(dic[1]) + " ***** " + str(dic[2])
            #print(str(current_id) + "\thas_dataset\t" + str(dic))
            print(finala)
        current_id = left_col
        dic = {}
        dic[0] = None
        dic[1] = None
        dic[2] = None
        if "has_data" in center_col:
            dic[0] = right_col
            continue
        elif "has_track" in center_col:
            dic[1] = right_col
            continue
        elif "has_award" in center_col:
            dic[2] = right_col
            continue
        continue

    if current_id == None:
        current_id = left_col

    if current_id == left_col:
        if "has_data" in center_col:
            dic[0] = right_col
            continue
        elif "has_track" in center_col:
            dic[1] = right_col
            continue
        elif "has_award" in center_col:
            dic[2] = right_col
            continue
    else:
        if len(dic) > 0:
            finala = str(dic[0]) + " ***** " + str(dic[1]) + " ***** " + str(dic[2])
            #print(str(current_id) + "\thas_dataset\t" + str(dic))
            print(finala)
        current_id = left_col
        dic = {}
        dic[0] = None
        dic[1] = None
        dic[2] = None
        if "has_data" in center_col:
            dic[0] = right_col
            continue
        elif "has_track" in center_col:
            dic[1] = right_col
            continue
        elif "has_award" in center_col:
            dic[2] = right_col
            continue
        continue    
