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
This reducer is used to process sorted data from the fifth mapper.
It does line by line and puts information about all the specific artists tracks together into one line.
'''

# Global variables initialization
current_id = None
data_list = list()

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
# Loop the input stream
for read_line in input_stream:
    read_line = read_line.strip()
    splitted_line = read_line.split("\t")

    left_col = splitted_line[0]
    center_col = splitted_line[1]

    # Is this line without ID ?
    if "None" in left_col:
        continue

    # Do we need this line?
    # Is it important or is it just a junk for us ?
    if current_id == None:
        current_id = left_col

    # If we found some information about our artists track (we stil operate with the same ID that belongs to some artist)
    if current_id == left_col:
        right_col = splitted_line[2]
        # Add the data to list if it is not already there
        if right_col not in data_list:
            data_list.append(right_col)
            continue
    # If we did not find the data to the artist we wanted
    else:
        # Reset everything but before that print out everything we collected
        # Is the list empty or do we need to print its content ?
        if len(data_list) > 0:
            print(str(current_id) + "\thas_track\t" + " ~~~ ".join(data_list))
        current_id = left_col
        data_list = list()
        data_list.append(right_col)
        continue    
