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
This mapper is used to process output from the first job and put all artist datas together
In the end, we get all artist personal data in one row.
'''

# Global variables initialization
FB_URL = 'http:\/\/rdf.freebase.com'
FB_NS_URL = 'http:\/\/rdf.freebase.com\/ns'
W3_URL = 'http:\/\/www.w3.org\/[0-9]*\/[0-9]*\/[0-9]*-*'


input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


current_id = None

dic = []
dic.append(None)
dic.append(None)
dic.append(None)
dic.append(None)

flag = 0

dic_o = []
dic_o.append(None)
dic_o.append(None)
dic_o.append(None)
dic_o.append(None)

current_col = None

# Loop the input stream
for read_line in input_stream:
    # Check if the line is not empty
    if len(read_line.strip()) == 0 :
        continue
    # Clean the line, get rid of unwanted strings
    original_line = read_line.strip()
    splitted_original_line = original_line.split("\t")
    read_line = re.sub(FB_NS_URL, '', read_line)
    read_line = re.sub(FB_URL, '', read_line)
    read_line = re.sub(W3_URL, '', read_line)
    read_line = read_line.replace("<", "")
    read_line = read_line.replace(">", "")
    read_line = read_line.replace("/", "")
    splitted_line = read_line.split("\t")
    left_col = splitted_line[0]
    center_col = splitted_line[1]
    left_col_original = splitted_original_line[0]
    center_col_original = splitted_original_line[1]

    # If we found some artists ID
    if ("an_artist" in center_col):
        # If the dictionary is not empty and we are not dealing with junk, print it out
        if len(dic) > 0 and current_id != None:
            temp = dic[0]
            print(str(temp) + "\thas_data\t" + "{" + str(dic[1]).encode("utf-8", "ignore").decode("ascii", "ignore") + " --- " + str(dic[2]).encode("utf-8", "ignore").decode("ascii", "ignore") + " --- " + str(dic[3]).encode("utf-8", "ignore").decode("ascii", "ignore") + "}")
        # Reset everything and set default values
        current_id = left_col_original
        dic = []
        dic.append(None)
        dic.append(None)
        dic.append(None)
        dic.append(None)
        dic[0] = current_id
        continue

    # Do we need this line?
    # Is it important or is it just a junk for us ?
    if current_id == None:
        print(original_line)
        continue

    # If we found some information about our artist (we stil operate with the same ID that belongs to some artist)
    if current_id == left_col_original:
        # Check the relation and based on that store data to dictionary
        right_col_original = splitted_original_line[2]
        if "has_name" in center_col:
            dic[1] = right_col_original
        if "has_description" in center_col:
            dic[2] = right_col_original
        if "was_born_at" in center_col:
            dic[3] = right_col_original
    # If we did not find the data we wanted
    else:
        # Reset everything but before that print out everything we collected
        temp = dic[0]
        print(str(temp) + "\thas_data\t" + "{" + str(dic[1]).encode("utf-8", "ignore").decode("ascii", "ignore") + " --- " + str(dic[2]).encode("utf-8", "ignore").decode("ascii", "ignore") + " --- " + str(dic[3]).encode("utf-8", "ignore").decode("ascii", "ignore") + "}")
        current_id = left_col_original
        dic = []
        dic.append(None)
        dic.append(None)
        dic.append(None)
        dic.append(None)
        dic[0] = current_id
        current_col = center_col
        continue
