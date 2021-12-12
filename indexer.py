import os
import sys
import io
from pathlib import Path

import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory

'''
This code is used to index the "final_jobs_output" file.
It goes line by line, with each line containing a cluster of complete information about one entity, ie 1 line in the file = 1 line in the indexed document.
This input file is read in a cycle, broken into pieces, and then this data is indexed.
'''

# Global variables initialization
env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])

fsDir = SimpleFSDirectory(Paths.get('index'))
ixAnalyzer = StandardAnalyzer()
ixConfig = IndexWriterConfig(ixAnalyzer)
ixConfig.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
ixWriter = IndexWriter(fsDir, ixConfig)

# Loop the input stream
with open("final_jobs_output") as f:
    for line in f:
        # Initialize lists
        track_names = list()
        track_other_datas = list()
        award_names = list()
        award_other_datas = list()
        line = line.strip()
        # Split line to parts
        line_parts = line.split(" ***** ")
        # Check if the tracks have some data
        if "None" not in line_parts[3] or line_parts[3].replace(" ", "").replace("\t", "") != "":
            track_datas = line_parts[3].split(" ~~~ ")
            # Loop through that data
            for data in track_datas:
                data_pieces = data.split(" --- ")
                # If there is the data we need
                if len(data_pieces) == 2:
                    # Add names to the list
                    track_names.append(data_pieces[0])
                    # And then add complete data to the other list (name with length)
                    tmp = " ~~~ ".join(data_pieces)
                    track_other_datas.append(tmp)
        # Check if the awards have some data
        if "None" not in line_parts[4] or line_parts[4].replace(" ", "").replace("\t", "") != "":
            award_datas = line_parts[4].split(" ~~~ ")
            # Loop through that data
            for data in award_datas:
                data_pieces = data.split(" --- ")
                # If there is the data we need
                if len(data_pieces) >= 2:
                    # Add names to the list
                    award_names.append(data_pieces[0])
                    # And then add complete data to the other list (description with honor year)
                    tmp = " ~~~ ".join(data_pieces)
                    award_other_datas.append(tmp)

        # Create a document for indexing purposes
        doc = Document()
        # Add fields to the document and fill them with the data we received
        doc.add(Field("artist_name", line_parts[0], TextField.TYPE_STORED))
        doc.add(Field("artist_description", line_parts[1], TextField.TYPE_STORED))
        doc.add(Field("artist_bday", line_parts[2], TextField.TYPE_STORED))
        t_names = " ***** ".join(track_names)
        doc.add(Field("track_names", t_names, TextField.TYPE_STORED))
        t_datas = " ***** ".join(track_other_datas)
        doc.add(Field("track_datas", t_datas, TextField.TYPE_STORED))
        a_names = " ***** ".join(award_names)
        doc.add(Field("award_names", a_names, TextField.TYPE_STORED))
        a_datas = " ***** ".join(award_other_datas)
        doc.add(Field("award_datas", a_datas, TextField.TYPE_STORED))
        # Write it to the document
        ixWriter.addDocument(doc)

        # Reset everything
        track_names = list()
        track_other_datas = list()
        award_names = list()
        award_other_datas = list()

# Commit everything and close the index writer
ixWriter.commit()
ixWriter.close()

