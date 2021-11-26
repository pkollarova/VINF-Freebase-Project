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

FB_URL = 'http:\/\/rdf.freebase.com'
FB_NS_URL = 'http:\/\/rdf.freebase.com\/ns'
W3_URL = 'http:\/\/www.w3.org\/[0-9]*\/[0-9]*\/[0-9]*-*'

#ids_list = list()

#output_file = open("job_1/mapper_output" ,"w", encoding="UTF-8")

#start_time = time.perf_counter ()

#read_file = open("../freebase-head-1000000" ,"r", encoding="UTF-8")
#read_line = read_file.readline()
input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
#for read_line in sys.stdin:
for read_line in input_stream:
#while read_line:
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
    string_1 = ""
    string_2 = ""
    string_2_addon = ""
    string_3 = ""
    string_3_addon = ""
    string_4 = ""
    if (right_col == "music.artist" and center_col == "type.object.type"):
        print(left_col_original + "\tan_artist")
#        output_file.write(string_1 + '\n')
        #ids_list.append(left_col)
    if center_col == "common.topic.description":
        print(left_col_original + "\thas_description\t" + right_col_original.encode("utf-8", "ignore").decode("ascii", "ignore"))
    if center_col == "people.person.date_of_birth":
        print(left_col_original + "\twas_born_at\t" + right_col_original.encode("utf-8", "ignore").decode("ascii", "ignore"))
#    if right_col == "music.recording":
#        string_2 = left_col_original + "\tis_track\t"
#    if (center_col == "music.artist.track"):
#        print(left_col_original + "\thas_track\t" + right_col_original.encode("utf-8", "ignore").decode("ascii", "ignore"))
#        string_2 = left_col_original + "\thas_track\t" + right_col_original
#        string_2_addon = right_col_original + "\tis_track"
#        output_file.write(string_2_addon + '\n')
#        output_file.write(string_2 + '\n')
        #ids_list.append(right_col)
#    if (center_col == "award.award_winner.awards_won"):
#        string_3 = left_col_original + "\thas_award\t" + right_col_original
#        string_3_addon = right_col_original + "\tis_award"
#        output_file.write(string_3_addon + '\n')
#        output_file.write(string_3 + '\n')
        #ids_list.append(right_col)
    if (("type.object.name" in center_col or "schema#label" in center_col)):
        print(left_col_original + "\thas_name\t" + right_col_original.encode("utf-8", "ignore").decode("ascii", "ignore"))
#        output_file.write(string_4 + '\n')
#        string_4 = original_line
#    if (string_1 is not ""):
#        print(string_1.encode("utf-8", "ignore").decode("ascii", "ignore"))
        #print('%s' % (string_1))
#    if (string_2_addon is not ""):
#        print(string_2_addon.encode("utf-8", "ignore").decode("ascii", "ignore"))
        #print('%s' % (string_2_addon))
#    if (string_2 is not ""):
#        print(string_2.encode("utf-8", "ignore").decode("ascii", "ignore"))
#    if (string_3_addon is not ""):
#        print(string_3_addon.encode("utf-8", "ignore").decode("ascii", "ignore"))
        #print('%s' % (string_3_addon))
#    if (string_3 is not ""):
#        print('%s' % (string_3))
#    if (string_4 is not ""):
#        print(string_4.encode("utf-8", "ignore").decode("ascii", "ignore"))
        #print(string_4)
    
#    read_line = read_file.readline()
#read_file.close()

#end_time = time.perf_counter ()
#print(end_time - start_time, "seconds")
#output_file.close()
