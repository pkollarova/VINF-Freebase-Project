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

env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])

fsDir = SimpleFSDirectory(Paths.get('index'))
ixAnalyzer = StandardAnalyzer()
ixConfig = IndexWriterConfig(ixAnalyzer)
ixConfig.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
ixWriter = IndexWriter(fsDir, ixConfig)


with open("final_jobs_output") as f:
    for line in f:
        track_names = list()
        track_other_datas = list()
        award_names = list()
        award_other_datas = list()
        line = line.strip()
        line_parts = line.split(" ***** ")
        #print(line_parts)
        if "None" not in line_parts[3] or line_parts[3].replace(" ", "").replace("\t", "") != "":
            track_datas = line_parts[3].split(" ~~~ ")
            for data in track_datas:
                data_pieces = data.split(" --- ")
                if len(data_pieces) == 2:
                    track_names.append(data_pieces[0])
                    tmp = " ~~~ ".join(data_pieces)
                    track_other_datas.append(tmp)
                    #if "Defecto Deserie" in line_parts[0]:
                        #print(track_other_datas)
        if "None" not in line_parts[4] or line_parts[4].replace(" ", "").replace("\t", "") != "":
            award_datas = line_parts[4].split(" ~~~ ")
            for data in award_datas:
                data_pieces = data.split(" --- ")
                if len(data_pieces) >= 2:
                    award_names.append(data_pieces[0])
                    tmp = " ~~~ ".join(data_pieces)
                    award_other_datas.append(tmp)
        doc = Document()
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
        ixWriter.addDocument(doc)

        track_names = list()
        track_other_datas = list()
        award_names = list()
        award_other_datas = list()


ixWriter.commit()
ixWriter.close()

