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

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
for read_line in input_stream:
#for read_line in sys.stdin:
    read_line = read_line.strip()
    splitted_line = read_line.split("\t")
    left_col = splitted_line[0]
    center_col = splitted_line[1]
    #right_col = splitted_line[2]
    

    if current_id == None:
        current_id = left_col

    if current_id == left_col:
        right_col = splitted_line[2]
        if right_col not in data_list:
            data_list.append(right_col)
            continue
    else:
        if len(data_list) > 0:
            print(str(current_id) + "\thas_track\t" + " ~~~ ".join(data_list))
        current_id = left_col
        data_list = list()
        data_list.append(right_col)
        continue    
