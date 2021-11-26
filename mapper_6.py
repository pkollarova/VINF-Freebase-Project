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

current_id = None

dic = []
dic.append(None)
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
   # right_col = splitted_line[2]
    left_col_original = splitted_original_line[0]
    center_col_original = splitted_original_line[1]
   # right_col_original = splitted_original_line[2]


    if ("an_award" in center_col):
        if len(dic) > 0 and current_id != None:
           #print(str(dic).encode("utf-8", "ignore").decode("ascii", "ignore"))
            #temp = str(dic[4])[2:]
            #temp_len = len(temp)
            #temp = temp[:temp_len - 2]
            temp = dic[4]
            print(str(temp) + "\thas_award\t" + "{" + str(dic[0]) + " --- " + str(dic[1]).encode("utf-8", "ignore").decode("ascii", "ignore") + " --- " + str(dic[2]).encode("utf-8", "ignore").decode("ascii", "ignore") + " --- " + str(dic[3]).encode("utf-8", "ignore").decode("ascii", "ignore") +  "}")
        current_id = left_col_original
        dic = []
        dic.append(None)
        dic.append(None)
        dic.append(None)
        dic.append(None)
        dic.append(None)
        dic[0] = current_id
        continue

    if current_id == None:
        print(original_line)
        continue

    if current_id == left_col_original:
        right_col_original = splitted_original_line[2]
        if "has_name" in center_col:
            dic[1] = right_col_original
        if "has_notes_description" in center_col:
            dic[2] = right_col_original
        if "was_honored_at" in center_col:
            dic[3] = right_col_original
        if "is_award_of" in center_col:
            dic[4] = right_col_original
    else:
        # print(str(dic).encode("utf-8", "ignore").decode("ascii", "ignore"))
        #temp = str(dic[4])[2:]
        #temp_len = len(temp)
        #temp = temp[:temp_len - 2]
        temp = dic[4]
        print(str(temp) + "\thas_award\t" + "{" + str(dic[0]) + " --- " + str(dic[1]).encode("utf-8", "ignore").decode("ascii", "ignore") + " --- " + str(dic[2]).encode("utf-8", "ignore").decode("ascii", "ignore") + " --- " + str(dic[3]).encode("utf-8", "ignore").decode("ascii", "ignore") +  "}")
        #print(str(temp) + "\thas_award\t" + "{" + str(dic[0]) + " --- " + str(dic[1]) + " --- " + str(dic[2]) + " --- " + str(dic[3]) + "}")
        current_id = left_col_original
        dic = []
        dic.append(None)
        dic.append(None)
        dic.append(None)
        dic.append(None)
        dic.append(None)
        dic[0] = current_id
        current_col = center_col
        continue
