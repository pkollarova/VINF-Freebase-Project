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
data_list = list()

FB_URL = 'http:\/\/rdf.freebase.com'
FB_NS_URL = 'http:\/\/rdf.freebase.com\/ns'
W3_URL = 'http:\/\/www.w3.org\/[0-9]*\/[0-9]*\/[0-9]*-*'

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
# Loop the input stream
for read_line in input_stream:
    # Clean the line, replace or remove unwanted strings
    read_line = read_line.strip()
    read_line = re.sub(FB_NS_URL, '', read_line)
    read_line = re.sub(FB_URL, '', read_line)
    read_line = re.sub(W3_URL, '', read_line)
    read_line = read_line.replace("<", "")
    read_line = read_line.replace(">", "")
    read_line = read_line.replace("/", "")
    read_line = read_line.replace("^", "")
    read_line = re.sub('http:www.w3.org[0-9]*XMLSchema#[date|gYear]*>', "", read_line)
                      
    splitted_line = read_line.split("\t")
    dataset = splitted_line[0]

    # Split the whole dataset to parts
    splitted_dataset =  dataset.split(" ***** ")
    # Initialize artist variables, where we will store the data
    personal_data = splitted_dataset[0].replace("{", "").replace("}", "")
    personal_data_splitted = personal_data.split(" --- ")
    personal_data_names = ""
    personal_data_desc = ""
    personal_data_born = ""

    # Initialize and fill track variables, where we will store the data
    track_data = ""
    track_data = splitted_dataset[1].replace("{", "").replace("}", "")

    # Initialize and fill award variables, where we will store the data
    award_data = ""
    award_data = splitted_dataset[2].replace("{", "").replace("}", "")
    
    # Loop the artist data (there may be a lot of data)
    for i in range(len(personal_data_splitted)):
        # Based on loop index save the data to the correct variable
        if i == 0:
            personal_data_names = personal_data_splitted[i]
        if i == 1:
            personal_data_desc = personal_data_splitted[i]
        if i == 2:
            personal_data_born = personal_data_splitted[i]
    # If there are absolutelly no names of the artist, skip this line because this information is important and without it we do not need to store this data
    if str(personal_data_names) == "None":
        continue
    # Then print out final data of some artist
    print(personal_data_names + " ***** " + personal_data_desc + " ***** " + personal_data_born + " ***** " + track_data + " ***** " + award_data)


