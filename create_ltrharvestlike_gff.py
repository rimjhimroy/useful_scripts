#!/usr/bin/env python


#Script to merge internal regions of LTRRTs with their LTRs and prepare an LTRharvest like gff file to be loaded into LTRdigest
#important to extract RT and other domains using hmm approach of LTRdigest
# the script requires Repbase fasta names to be modified in the format '_internal' or '_LTR': for example internal regions in repbase with names like 'ATGP10_I' or 'ATGP10-I' or 'Gypsy20-I_Aly' or 'Gypsy20_I_Aly' to be named as ATGP10_internal' and 'Gypsy20_Aly_internal'. Same goes for LTRs e.g. 'ATGP10-LTR' becomes 'ATGP10_LTR'
# run the script like: create_ltrharvestlike_gff.py internal.fas LTR.fas name
# e.g. for Rosids: create_ltrharvestlike_gff.py Rosids.internal.fas Rosids.LTR.fas Rosids

from Bio import SeqIO
import re,os
import sys

inters = list(SeqIO.parse(sys.argv[1], 'fasta'))
ltrs=list(SeqIO.parse(sys.argv[2], 'fasta'))
full=open(sys.argv[3]+'.Repbasefull.fasta','w')
ini=open('ltrharvestlike.initial','w')
mid=open('ltrharvestlike.mid','w')
main=open('ltrharvestlike.main','w')
ini.write('##gff-version   3\n')

c=0
for inter in inters:
	for ltr in ltrs:
		inid=re.split('_internal',inter.id)[0]
		ltrid=re.split('_LTR',ltr.id)[0]
		#print inid,ltrid
		if inid==ltrid:
			c+=1
			
			full.write('>'+ltrid+'\n')
			ltrseq=str(ltr.seq)
			intseq=str(inter.seq)
			nseq=ltrseq+intseq+ltrseq
			full.write(nseq+'\n')
			ini.write('##sequence-region   '+ltrid+' 1 '+str(len(nseq))+'\n')
			print inid, len(nseq), len(ltrseq),len(ltrseq),len(intseq)
			mid.write('#'+ltrid+'\n')
			main.write(ltrid+'\tLTRharvest\trepeat_region\t1\t'+str(len(nseq))+'\t.\t?\t.\tID=repeat_region'+str(c)+'\n')
			main.write(ltrid+'\tLTRharvest\tinverted_repeat\t1\t2\t.\t?\t.\tParent=repeat_region'+str(c)+'\n')
			main.write(ltrid+'\tLTRharvest\tLTR_retrotransposon\t1\t'+str(len(nseq))+'\t.\t?\t.\tID=LTR_retrotransposon'+str(c)+';Parent=repeat_region'+str(c)+';ltr_similarity=100.00;seq_number='+str(c-1)+'\n')
			main.write(ltrid+'\tLTRharvest\tlong_terminal_repeat\t1\t'+str(len(ltrseq))+'\t.\t?\t.\tParent=LTR_retrotransposon'+str(c)+'\n')
			main.write(ltrid+'\tLTRharvest\tlong_terminal_repeat\t'+str(len(nseq)-len(ltrseq)+1)+'\t'+str(len(nseq))+'\t.\t?\t.\tParent=LTR_retrotransposon'+str(c)+'\n')
			main.write(ltrid+'\tLTRharvest\tinverted_repeat\t'+str(len(nseq)-1)+'\t'+str(len(nseq))+'\t.\t?\t.\tParent=repeat_region'+str(c)+'\n')
			main.write('###\n')
			break
		
ini.close()
mid.close()
main.close()
#Concatenate
gff=open('LTRlist.gff','w')
ini=open('ltrharvestlike.initial','r')
mid=open('ltrharvestlike.mid','r')
main=open('ltrharvestlike.main','r')
gff.write(ini.read())
ini.close()
gff.write(mid.read())
mid.close()
gff.write(main.read())
main.close()
os.remove("ltrharvestlike.initial")
os.remove("ltrharvestlike.mid")
os.remove("ltrharvestlike.main")

