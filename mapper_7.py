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
dic = {}
dic[0] = None
dic[1] = None
dic[2] = None

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

for read_line in input_stream:
#for read_line in sys.stdin:
    if len(read_line.strip()) == 0 :
        continue
    original_line = read_line.strip()
    splitted_original_line = original_line.split("\t")
    print(original_line)
