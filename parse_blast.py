#!/usr/bin/env python3
from blast import parse
import os
import sys
import argparse

print()

# create variables that can be entered as arguments in command line
parser = argparse.ArgumentParser(
    description='This script takes a blast output in -outfmt 6/ -m8 format and parses it based on several parameters')
parser.add_argument('-file', type=str, metavar='blast_output',
                    required=True, help='REQUIRED: Full path to blast output')
parser.add_argument('-evalue', type=str, metavar='evalue_cutoff',
                    default='1e-6', help='Evalue cutoff (string) [1e-6]')
parser.add_argument('-identity', type=float, metavar='identity_cutoff',
                    default=80, help='Minimum identity cutoff (integer) [80]')
parser.add_argument('-length', type=int, metavar='alignment_length',
                    default=80, help='Minimum alignment length cutoff [80]')
args = parser.parse_args()
fh = open(args.file)
outfile = os.path.basename(args.file)+".bastout"
outf = open(outfile, "w+")
for blast_record in parse(fh):
    header = ['querry', 'subject', 'length', 'evalue',
              'qstart', 'qend', 'hstart', 'hend', 'perc_identity']
    outf.write('\t'.join(header[0:])+'\n')
    for hit in blast_record.hits:
        for hsp in hit:
            if hsp.evalue < float(args.evalue) and hsp.pident > args.identity and hsp.length > args.length:
                records = [hsp.qid, hsp.sid, hsp.length, hsp.evalue,
                           hsp.qstart, hsp.qend, hsp.sstart, hsp.send, hsp.pident]
                outf.write('\t'.join(map(str, records[0:])) + '\n')
outf.close()
fh.close()
