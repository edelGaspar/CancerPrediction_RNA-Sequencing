#!/usr/bin/env python
# coding: utf-8

# Imports
import gzip
import shutil
import gffutils
import os

class MappingGff3:
    
    def __init__(self, gff3_path):
        self.gff3_path = gff3_path
        self.gff3_file = gff3_path.rsplit('.', 1)[0]

    def generate_gff3_db(self):
        if not 'db' in dir(self):
            with gzip.open(self.gff3_path, 'rb') as f_in:
                with open(self.gff3_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            self.db = gffutils.create_db(self.gff3_file, ":memory:", merge_strategy='create_unique', id_spec={'gene': 'gene_id', 'transcript': 'transcript_id'})
        
    def get_length_gene_kb(self, gene_id, method='max'):
        transcript_count = 0
        summation = 0
        result = 0
        c = self.db.conn.cursor()
        c.execute(f"SELECT id FROM features WHERE id like '{gene_id}.%'")
        id_version = c.fetchone()[0]
        for child_transcript in self.db.children(id_version, 1, featuretype='transcript'):
            transcript_count += 1
            axon_sum = sum((exon.stop - exon.start)/1000 for exon in self.db.children(child_transcript.id, 1, featuretype='exon'))
            match method:
                case 'max':
                    result = result if result > axon_sum else axon_sum
                case 'min':
                    if result == 0:
                        result = axon_sum
                    else:
                        result = result if result < axon_sum else axon_sum
                case 'mean':
                    summation += axon_sum
                    result = (summation)/transcript_count
        return result