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
parser.add_argument('-blastout', type=str, metavar='blast_output_path',
                    default="./outblast", help='full path to blast output folder to store in -outfmt 6/ -m8 format [./outblast]')
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

outname = os.path.basename(args.query)+'_'+os.path.basename(args.subject)
if not os.path.exists(args.blastout):
    os.mkdir(args.blastout)
if args.program == "megablast":
    outpath = args.blastout+'/'+outname+'.megablast.out'
    cmd = ('megablast -d '+args.subject+' -i' +
           args.query+' -m 8 -o '+outpath)
    p = subprocess.Popen(cmd, shell=True)
    sts = os.waitpid(p.pid, 0)[1]
elif args.program == "blastn":
    outpath = args.blastout+'/'+outname+'.blastn.out'
    cmd = ('blastn -db '+args.subject+' -query ' +
           args.query+' -outfmt 6 -out '+outpath)
    p = subprocess.Popen(cmd, shell=True)
    sts = os.waitpid(p.pid, 0)[1]

'''
if not os.path.exists(args.blastout+"/pickle"):
    os.mkdir(args.blastout+"/pickle")
pickle_out1 = open(args.blastout+"/pickle/save.p1", "wb")
pickle.dump(outpath, pickle_out1)
pickle_out1.close()
blastout = open(args.blastout+"/pickle/save.p1", "rb")
fh = pickle.load(blastout)
'''

fh = open(outpath)
outfile = args.blastout+'/' + \
    os.path.basename(outname)+".filtered."+args.program+".out"
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
