import os
import sys
import io
from pathlib import Path
import argparse

import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

'''
This code is used for index searches.
At the input, we will receive a search query in the arguments, which we will search for and display its results.
'''

# Get the query from arguments
argParser = argparse.ArgumentParser()
argParser.add_argument('searched_data', type=str)
args = argParser.parse_args()

env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Find index and setup some variables
fsDir = SimpleFSDirectory(Paths.get('index'))
ixAnalyzer = StandardAnalyzer()
ixSearcher = IndexSearcher(DirectoryReader.open(fsDir))

# Search that query
ixParser = QueryParser("default_field", ixAnalyzer)
query = ixParser.parse(args.searched_data)

# Get the hits from searching
hits = ixSearcher.search(query, 10).scoreDocs

print("\n")
print("**********************")
print("*** SEARCH RESULTS ***")
print("**********************")
print("\n")

# Loop the hits
for hit in hits:
    # Get the found data and print it
    hitDoc = ixSearcher.doc(hit.doc)
    print("Artist Name(s)")
    print("\t" + hitDoc.get("artist_name"))
    print("Artist Description")
    print("\t" + hitDoc.get("artist_description"))
    print("Artist Birthday")
    print("\t" + hitDoc.get("artist_bday").replace("http:www.w3.org2001XMLSchema#date", "").replace("http:www.w3.org2001XMLSchema#gYear", ""))
    print("Artist Track(s) - Name + Length")
    separate_track_data = hitDoc.get("track_datas").split("*****")
    # If there are any track data, print them out one by one
    if separate_track_data != None:
        for el in separate_track_data:
            print("\t" + el.replace("\t", " "))
    print("Artist Award(s) - Description + Year")
    separate_award_data = hitDoc.get("award_datas").split("*****")
    # If there are any award data, print them out one by one
    if separate_award_data != None:
        for el in separate_award_data:
            print("\t" + el.replace("http:www.w3.org2001XMLSchema#gYear", "").replace("\t", " "))
    print("\n\n\n")
