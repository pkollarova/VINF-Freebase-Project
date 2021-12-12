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

'''
This reducer is used to process sorted data from the seventh mapper.
It does line by line and puts every information about the specific artist together into one line.
'''

# Global variables initialization
current_id = None
data_list = list()
dic = {} 
dic[0] = None
dic[1] = None
dic[2] = None
finala = ""

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# Loop the input stream
for read_line in input_stream:
    read_line = read_line.strip()
    splitted_line = read_line.split("\t")
    left_col = splitted_line[0]
    center_col = splitted_line[1]
    right_col = splitted_line[2]

    # If we found a line without artist ID
    if str(current_id) == "None":
        # If there is some data in the dictionary, print it out
        if len(dic) > 0:
            finala = str(dic[0]) + " ***** " + str(dic[1]) + " ***** " + str(dic[2])
            print(finala)
        # Now reset everything
        current_id = left_col
        dic = {}
        dic[0] = None
        dic[1] = None
        dic[2] = None
        # Check the current relation and based on that fill data to the dictionary
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

    # Do we need this line?
    # Is it important or is it just a junk for us ?
    if current_id == None:
        current_id = left_col

    # If we found some information about our artist we were looking for (we stil operate with the same ID that belongs to some artist)
    if current_id == left_col:
        # Fill in the dictionary based on the relation
        if "has_data" in center_col:
            dic[0] = right_col
            continue
        elif "has_track" in center_col:
            dic[1] = right_col
            continue
        elif "has_award" in center_col:
            dic[2] = right_col
            continue
    # If we did not find the data to the artist we wanted
    else:
        # If there is some data in the dictionary, print it out
        if len(dic) > 0:
            finala = str(dic[0]) + " ***** " + str(dic[1]) + " ***** " + str(dic[2])
            print(finala)
        # Now reset everything
        current_id = left_col
        dic = {}
        dic[0] = None
        dic[1] = None
        dic[2] = None
        # Check the current relation and based on that fill data to the dictionary
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
