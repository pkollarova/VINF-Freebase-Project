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
FB_URL = 'http:\/\/rdf.freebase.com'
FB_NS_URL = 'http:\/\/rdf.freebase.com\/ns'
W3_URL = 'http:\/\/www.w3.org\/[0-9]*\/[0-9]*\/[0-9]*-*'


input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
# Loop the input stream
for read_line in input_stream:
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
    right_col = splitted_line[2]
    left_col_original = splitted_original_line[0]
    center_col_original = splitted_original_line[1]
    right_col_original = splitted_original_line[2]

    # If we found any music artists track
    if (center_col == "music.artist.track"):
        print(right_col_original + "\ta_track")
        print(right_col_original + "\tis_track_of\t" + left_col_original)
    # If we found any music recordings length
    if center_col == "music.recording.length":
        print(left_col_original + "\thas_length\t" + right_col_original)
    # If we found any name or label
    if (("type.object.name" in center_col or "schema#label" in center_col)):
        print(left_col_original + "\thas_name\t" + right_col_original.encode("utf-8", "ignore").decode("ascii", "ignore"))