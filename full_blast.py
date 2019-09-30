#!/usr/bin/env python3
from blast import parse
import os
import sys
import subprocess
import argparse
import pickle

print()

# create variables that can be entered as arguments in command line
parser = argparse.ArgumentParser(
    description='This script takes a query and a database file for blast/megablast and parses it')
parser.add_argument('-query', type=str, metavar='blast_query',
                    required=True, help='REQUIRED: Full path to query file')
parser.add_argument('-subject', type=str, metavar='blast_subject',
                    required=True, help='REQUIRED: Full path to subject file')
parser.add_argument('-program', type=str, metavar='blast_program',
                    required=True, help='REQUIRED: blast program to use blastn/megablast')
parser.add_argument('-blastout', type=str, metavar='blast_output',
                    required=True, help='REQUIRED: full path to blast output filename to store in -outfmt 6/ -m8 format')
parser.add_argument('-evalue', type=str, metavar='evalue_cutoff',
                    default='1e-6', help='Evalue cutoff (string) [1e-6]')
parser.add_argument('-identity', type=float, metavar='identity_cutoff',
                    default=80, help='Minimum identity cutoff (integer) [80]')
parser.add_argument('-length', type=int, metavar='alignment_length',
                    default=80, help='Minimum alignment length cutoff [80]')
args = parser.parse_args()

cmd = ('makeblastdb -dbtype nucl -parse_seqids -in '+args.subject)
p = subprocess.Popen(cmd, shell=True)
sts = os.waitpid(p.pid, 0)[1]

if args.program == "megablast":
    cmd = ('megablast -d '+args.subject+' -i' +
           args.query+' -m 8 -o '+args.blastout)
    p = subprocess.Popen(cmd, shell=True)
    sts = os.waitpid(p.pid, 0)[1]
elif args.program == "blastn":
    cmd = ('blastn -db '+args.subject+' -query ' +
           args.query+' -outfmt 6 -out '+args.blastout)
    p = subprocess.Popen(cmd, shell=True)
    sts = os.waitpid(p.pid, 0)[1]

pickle.dump(args.blastout, open(os.path.dirname(args.blastout)+"/save.p1", "wb"))
blastout = pickle.load(open(os.path.dirname(args.blastout)+"/save.p1", "rb"))
fh = open(blastout)
outfile = os.path.dirname(args.blastout)+'/'+os.path.basename(args.blastout)+".blastout"
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
