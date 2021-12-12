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
This mapper is used just to print out all data from input, so then they can be sorted.
This mapper is very trivial.
'''

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# Loop the input stream
for read_line in input_stream:
    # Check if the line is not empty
    if len(read_line.strip()) == 0 :
        continue
    # Edit the line a bit and print it out
    original_line = read_line.strip()
    splitted_original_line = original_line.split("\t")
    print(original_line)
