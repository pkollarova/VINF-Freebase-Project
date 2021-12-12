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

# Global variables initialization
current_id = None
name_list = list()
current_relation = None
names = ""

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
# Loop the input stream
for read_line in input_stream:
    original_line = read_line
    read_line = read_line.strip()
    splitted_line = read_line.split("\t")
    left_col = splitted_line[0]
    center_col = splitted_line[1]
    right_col = ""
    
    # Check if there is an award on this line
    # If yes, print it out
    if center_col == "an_award":
        if len(name_list) > 0:
            print(str(current_id) + "\t" + str(current_relation) + "\t" + " ~~~ ".join(name_list))
        current_id = left_col
        current_relation = None
        print(left_col + "\tan_award")
        continue

    # Do we need this line?
    # Is it important or is it just a junk for us ?
    if current_id == None and current_relation == None:
        name_list = list()
        names = ""
        continue

    # If we found some information about our award (we stil operate with the same ID that belongs to some award)
    if current_id == left_col:
        # If we did not find the relation between award and data we were looking for
        if current_relation == None:
            name_list = list()
            names = ""
            current_relation = center_col
        # If we did
        if current_relation == center_col:
            # Add the data to list if it is not already there
            if splitted_line[2] not in name_list:
                name_list.append(splitted_line[2])
                names += splitted_line[2] + " ~~~ "
            continue
        # If we did not find the data we wanted (limit case)
        else:
            # Reset everything if the line is junk for us
            if current_id == None:
                current_relation = None
                name_list = list()
                names = ""
                continue
            # Reset everything but before that print out everything we collected
            print(str(current_id) + "\t" + str(current_relation) + "\t" + " ~~~ ".join(name_list))
            current_relation = center_col
            name_list = list()
            names = ""
            name_list.append(splitted_line[2])
            names += splitted_line[2] + " ~~~ "
            continue
    # If we did not find the data we wanted (normal case)
    else:
        # If the ID we are collecting data for is different but still is it some kind of award
        if center_col == "an_award":
            current_id = left_col
            print(left_col + "\tan_award")
            current_relation = None
            name_list = list()
            names = ""
            continue
        # Else if it is just junk
        else:
            # Reset everything but before that print out everything we collected
            if len(name_list) > 0:
                print(str(current_id) + "\t" + str(current_relation) + "\t" + " ~~~ ".join(name_list))
            current_id = None
            current_relation = None
            name_list = list()
            names = ""
            
