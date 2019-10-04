#!/usr/bin/env python3

# Writen by Rimjhim Roy Choudhury

import os
import sys
import subprocess
import argparse

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


print()


# create variables that can be entered as arguments in command line
parser = MyParser(argparse.ArgumentParser(description="This script takes a query and a database file for blastn/megablast and parses it"))
parser.add_argument("-q","--query", type=str, metavar='blast_query', required=True, help="REQUIRED: Full path to query file")
parser.add_argument("-s",'--subject', type=str, metavar='blast_subject',required=True, help='REQUIRED: Full path to subject file')
parser.add_argument("-p",'--program', type=str, metavar='blast_program',required=True, help='REQUIRED: blast program to use blastn/megablast')
parser.add_argument("-o",'--blastout', type=str, metavar='blast_output_path',default="./outblast", help='full path to blast output folder to store in -outfmt 6/ -m8 format [DEFAULT: ./outblast]')
parser.add_argument("-i",'--identity', type=float, metavar='identity_cutoff',default=80, help='Minimum identity cutoff in %% [DEFAULT: 80]')
parser.add_argument("-qc",'--querycov', type=float, metavar='query_coverage_cutoff',default=20, help='Minimum query coverage cutoff in %% [DEFAULT: 20]')
parser.add_argument("-l",'--hitlength', type=int, metavar='hit_length',default = 80, help = 'Minimum hit length cutoff in bps [DEFAULT: 80]')
parser.add_argument("-t",'--num_threads', type = int, metavar = 'number_of_threads',default = 4, help = 'Maximum number of threads [DEFAULT: 4]')
args = parser.parse_args()

# make blast db
print("\n\nCreating BlastDB!!!\n\n")
cmdDB=('makeblastdb -dbtype nucl -parse_seqids -in '+args.subject)
print(cmdDB)
p=subprocess.Popen(cmdDB, shell = True)
sts=os.waitpid(p.pid, 0)[1]

# run blast
print("\n\nRunning "+args.program+"!!!\n\n")
outname=os.path.splitext(os.path.basename(args.query))[
                         0]+'_'+os.path.splitext(os.path.basename(args.subject))[0]
if not os.path.exists(args.blastout):
    os.mkdir(args.blastout)
if args.program == "megablast":
    outpath= args.blastout+'/'+outname+'.megablast.out'
    cmdBlast = ('blastn -task megablast -db '+args.subject+' -query ' +
           args.query+' -outfmt 6 -out '+outpath+' -num_threads '+str(args.num_threads))
    print(cmdBlast)
    p1 = subprocess.Popen(cmdBlast, shell=True)
    sts = os.waitpid(p1.pid, 0)[1]
elif args.program == "blastn":
    outpath = args.blastout+'/'+outname+'.blastn.out'
    cmdBlast = ('blastn -task blastn -db '+args.subject+' -query ' +
           args.query+' -outfmt 6 -out '+outpath+' -num_threads '+str(args.num_threads))
    print(cmdBlast)
    p1 = subprocess.Popen(cmdBlast, shell=True)
    sts = os.waitpid(p1.pid, 0)[1]

'''
if not os.path.exists(args.blastout+"/pickle"):
    os.mkdir(args.blastout+"/pickle")
pickle_out1 = open(args.blastout+"/pickle/save.p1", "wb")
pickle.dump(outpath, pickle_out1)
pickle_out1.close()
blastout = open(args.blastout+"/pickle/save.p1", "rb")
fh = pickle.load(blastout)
'''
# Parse and filter blast
print ("\n\nFiltering Blast Results!!!\n\n")
cmdFilter = ('query_coverage.py -blout '+outpath+' -query '+args.query+' -identity '+str(args.identity)+' -querycov '+str(args.querycov)+' -hitlength '+str(args.querycov))
print(cmdFilter)
p2 = subprocess.Popen(cmdFilter, shell=True)
sts = os.waitpid(p2.pid, 0)[1]

