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

FB_URL = 'http:\/\/rdf.freebase.com'
FB_NS_URL = 'http:\/\/rdf.freebase.com\/ns'
W3_URL = 'http:\/\/www.w3.org\/[0-9]*\/[0-9]*\/[0-9]*-*'

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
for read_line in input_stream:
#for read_line in sys.stdin:
    read_line = read_line.strip()
    read_line = re.sub(FB_NS_URL, '', read_line)
    read_line = re.sub(FB_URL, '', read_line)
    read_line = re.sub(W3_URL, '', read_line)
    read_line = re.sub("http:\/\/www.w3.org\/[0-9]*\/XMLSchema#date>", "", read_line)
    read_line = read_line.replace("<", "")
    read_line = read_line.replace(">", "")
    read_line = read_line.replace("/", "")
    read_line = read_line.replace("^", "")
                      
    splitted_line = read_line.split("\t")
    artist_id = splitted_line[0]
    dataset = splitted_line[2]

    splitted_dataset =  dataset.split(" ***** ")
    personal_data = splitted_dataset[0].replace("{", "").replace("}", "")
    personal_data_splitted = personal_data.split(" --- ")
    personal_data_names = ""
    personal_data_desc = ""
    personal_data_born = ""

    track_data = ""
    track_data = splitted_dataset[1].replace("{", "").replace("}", "")

    award_data = ""
    award_data = splitted_dataset[2].replace("{", "").replace("}", "")
    
    for i in range(len(personal_data_splitted)):
        if i == 0:
            personal_data_names = personal_data_splitted[i]
        if i == 1:
            personal_data_desc = personal_data_splitted[i]
        if i == 2:
            personal_data_born = personal_data_splitted[i]
    print(artist_id + " ***** " + personal_data_names + " ***** " + personal_data_desc + " ***** " + personal_data_born + " ***** " + track_data + " ***** " + award_data)
    print("\n\n")

