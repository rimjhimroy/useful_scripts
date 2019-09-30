import sys, os, glob, shutil, getopt
import re
from Bio import SeqIO
import gffutils
from Bio.Seq import Seq
from docopt import docopt


def main(argv):
	genome = ''
	ltrdigest = ''
	myfasta = ''
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'g:d:f:', ['genome=', 'ltrdigest=', 'fasta='])
	except getopt.GetoptError:
		print "Error"
		print 'categoriseLTRelementsinfasta.py -g <genome> -d <ltrdigest_gff> -f <file ending with _complete.fas>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'categoriseLTRelementsinfasta.py -g <genome> -d <ltrdigest_gff> -f <file ending with _complete.fas>'
			sys.exit()
		elif opt in ("-g", "--genome"):
			genome = arg
		elif opt in ("-d", "--ltrdigest"):
			ltrdigest = arg
		elif opt in ("-f", "--fasta"):
			myfasta = arg
	print 'Genome file is "', genome
	print 'LTR digest file is "', ltrdigest
	print 'Complete LTR-RT fasta file is "', myfasta


	current=os.getcwd()

	db = gffutils.create_db(ltrdigest, ':memory:')
	os.chdir(current)
	#argum=argum+"/categorise"
	#os.chdir(argum)

	records = list(SeqIO.parse(myfasta, "fasta"))
	base=re.split(".fas",myfasta)[0]
	#base="Clust"+base
	path = os.path.join(base)

	if not os.path.exists(path): 
		os.makedirs(path)
	savedPath = os.getcwd()
	#print base
	os.chdir(base)
	basepath=os.getcwd()
	rec_dict = {}
	for record in records:
		limit = re.sub(r'(.*)_(\d+)_(\d+)', r'\1:\2-\3', record.id.rstrip())
		chrom=re.sub(r'(.*)_\d+_\d+', r'\1', record.id.rstrip())
		st = re.sub(r'.*_(\d+)_\d+', r'\1', record.id.rstrip())
		en = re.sub(r'.*_\d+_(\d+)', r'\1', record.id.rstrip())
		#print limit

		for rec in db.all_features(limit,featuretype='LTR_retrotransposon'):
			#print rec.start, rec.stop
			if str(rec.start)==str(st) and str(rec.stop)==str(en):
				#print rec
				rec_dict[record.id.rstrip()]=str(*rec.attributes['ID'])
				#print parent


	for record in records:
		my_type = {'RT': ''}
		my_seq={'RT': ''}
		my_score={'RT': 1000}
		my_start={'RT': 0}
		my_end={'RT': 0}
		my_strand = {'RT':''}
		my_frame={'RT': 0}
		newseq=""
		'''
		os.chdir(digest)
		#Get best eval prot dom
		my_type = {'RT': '', 'GAG':'','AP':'','RNaseH':'','INT':'','ENV':''}
		my_seq={'RT': '', 'GAG':'','AP':'','RNaseH':'','INT':'','ENV':''}
		my_score={'RT': 1000, 'GAG':1000,'AP':1000,'RNaseH':1000,'INT':1000,'ENV':1000}
		my_start={'RT': 0, 'GAG':0,'AP':0,'RNaseH':0,'INT':0,'ENV':0}
		my_end={'RT': 0, 'GAG':0,'AP':0,'RNaseH':0,'INT':0,'ENV':0}
		my_strand = {'RT':'','GAG':'','AP':'','RNaseH':'','INT':'','ENV':''}
		my_frame={'RT': 0, 'GAG':0,'AP':0,'RNaseH':0,'INT':0,'ENV':0}
		my_prot={'RT': '', 'GAG':'','AP':'','RNaseH':'','INT':'','ENV':''}

		#(get LTR number:)
		for line in ltrtable:
			name=re.split('\t',line)
		
			if name[0]==record.id:
				nameltr= name[1]
				break;
		limit = re.sub(r'(.*)_(\d+)_(\d+)', r'\1:\2-\3', record.id.rstrip())
		chrom=re.sub(r'(.*)_\d+_\d+', r'\1', record.id.rstrip())
		print limit

		for rec in db.all_features(limit,featuretype='protein_match'):
			name=str(*rec.attributes['name'])
		
			dombase=re.split("_",name)[0]
			score=float(rec.score)
			
			if my_score[dombase]>score:
				my_frame[dombase]=int(*rec.attributes['reading_frame'])
				my_score[dombase]=rec.score
				my_type[dombase]=name
				my_start[dombase]=rec.start
				my_end[dombase]=rec.stop
				my_strand[dombase]=rec.strand
				my_seq[dombase]=Seq(rec.sequence(genome))

				protfile='LTRdigest_pdom_'+name+'_aa.fas'
						
				protrecs=list(SeqIO.parse(protfile, "fasta"))
				for protrec in protrecs:
					if protrec.id==record.id:
						
						my_prot[dombase]=str(protrec.seq)
						break
				
		#(test all doms are in same strand)
		testvalp='+'
		testvaln='-'
		
		
		os.chdir(basepath)

		if all(val==testvalp for val in my_strand.values() if val !=''): 
			for dom in my_type:
				if my_type[dom]!='':
					with open(dom+'ev_'+base+'_nuc.fas','a') as nhandle:
						nhandle.write(">"+record.id+'_'+my_type[dom]+'\n')
						nhandle.write(str(my_seq[dom])+'\n')
					with open(dom+'ev_'+base+'_prot.fas','a') as phandle:
						phandle.write(">"+record.id+'_'+my_type[dom]+'\n')
						phandle.write(my_prot[dom]+'\n')
		elif all(val==testvaln for val in my_strand.values() if val !=''): 
			for dom in my_type:
				if my_type[dom]!='':
					with open(dom+'ev_'+base+'_nuc.fas','a') as nhandle:
						n=my_seq[dom].reverse_complement()
						nhandle.write(">"+record.id+'_'+my_type[dom]+'\n')
						nhandle.write(str(n)+'\n')
					with open(dom+'ev_'+base+'_prot.fas','a') as phandle:
						phandle.write(">"+record.id+'_'+my_type[dom]+'\n')
						phandle.write(my_prot[dom]+'\n')
		
		else: print "confused\n"+str(my_strand)+'\n'
		

		
					
		
		#Get longest protein and nucleotide domains
		os.chdir(digest)
		my_type = {'RT': '', 'GAG':'','AP':'','RNaseH':'','INT':'','ENV':''}
		my_seq={'RT': '', 'GAG':'','AP':'','RNaseH':'','INT':'','ENV':''}
		my_len={'RT': 0, 'GAG':0,'AP':0,'RNaseH':0,'INT':0,'ENV':0}
		my_prot={'RT': '', 'GAG':'','AP':'','RNaseH':'','INT':'','ENV':''}
		for mynuc in glob.glob('*_pdom_*[!aa].fas'):
			nucrecs = list(SeqIO.parse(mynuc, "fasta"))
			for nucrec in nucrecs:
				if nucrec.id==record.id:
					nucbase=os.path.basename(re.split(".fas",mynuc)[0])
					nucbase=re.split("LTRdigest_pdom_",nucbase)[1]
					dombase=re.split("_",nucbase)[0]
					
					if my_len[dombase]<len(nucrec.seq):
						my_len[dombase]=len(nucrec.seq)
						my_type[dombase]=nucbase
						my_seq[dombase]=str(nucrec.seq)
						protfile='LTRdigest_pdom_'+nucbase+'_aa.fas'
						
						protrecs=list(SeqIO.parse(protfile, "fasta"))
						for protrec in protrecs:
							if protrec.id==record.id:
								
								my_prot[dombase]=str(protrec.seq)
								break
						
		os.chdir(basepath)
		
		if my_type['RT']!='':
			with open('RT_'+base+'_nuc.fas','a') as RT:
				RT.write(">"+record.id+'_'+my_type['RT']+'\n')
				RT.write(my_seq['RT']+'\n')
			with open('RT_'+base+'_prot.fas','a') as RT:
				RT.write(">"+record.id+'_'+my_type['RT']+'\n')
				RT.write(my_prot['RT']+'\n')
		if my_type['GAG']!='':
			with open('GAG_'+base+'_nuc.fas','a') as GAG:
				GAG.write(">"+record.id+'_'+my_type['GAG']+'\n')
				GAG.write(my_seq['GAG']+'\n')
			with open('GAG_'+base+'_prot.fas','a') as GAG:
				GAG.write(">"+record.id+'_'+my_type['GAG']+'\n')
				GAG.write(my_prot['GAG']+'\n')
		if my_type['AP']!='':
			with open('AP_'+base+'_nuc.fas','a') as AP:
				AP.write(">"+record.id+'_'+my_type['AP']+'\n')
				AP.write(my_seq['AP']+'\n')
			with open('AP_'+base+'_prot.fas','a') as AP:
				AP.write(">"+record.id+'_'+my_type['AP']+'\n')
				AP.write(my_prot['AP']+'\n')
		if my_type['RNaseH']!='':
			with open('RNaseH_'+base+'_nuc.fas','a') as RNaseH:
				RNaseH.write(">"+record.id+'_'+my_type['RNaseH']+'\n')
				RNaseH.write(my_seq['RNaseH']+'\n')
		if my_type['ENV']!='':
			with open('ENV_'+base+'_nuc.fas','a') as ENV:
				ENV.write(">"+record.id+'_'+my_type['ENV']+'\n')
				ENV.write(my_seq['ENV']+'\n')
			with open('ENV_'+base+'_prot.fas','a') as ENV:
				ENV.write(">"+record.id+'_'+my_type['ENV']+'\n')
				ENV.write(my_prot['ENV']+'\n')
		if my_type['INT']!='':
			with open('INT_'+base+'_nuc.fas','a') as INT:
				INT.write(">"+record.id+'_'+my_type['INT']+'\n')
				INT.write(my_seq['INT']+'\n')
			with open('INT_'+base+'_prot.fas','a') as INT:
				INT.write(">"+record.id+'_'+my_type['INT']+'\n')
				INT.write(my_prot['INT']+'\n')
		
		
		#Get full length sequences
		os.chdir(digest)
		
		for myfull in glob.glob('*_complete.fas'):
			fullseqs = list(SeqIO.parse(myfull, "fasta"))
			for fullseq in fullseqs:
				if fullseq.id==record.id:
					os.chdir(basepath)
					with open('FULLseq_'+base+'.fas','a') as full:
						full.write(">"+record.id+'_'+base+'\n')
						full.write(str(fullseq.seq)+'\n')
		
		
		#Get PBS
		os.chdir(digest)
		
		for mypbs in glob.glob('*_pbs.fas'):
			pbseqs = list(SeqIO.parse(mypbs, "fasta"))
			for pbseq in pbseqs:
				if pbseq.id==record.id:
					os.chdir(basepath)
					with open('PBSseq_'+base+'.fas','a') as pbs:
						pbs.write(">"+record.id+'\n')
						pbs.write(str(pbseq.seq)+'\n')
		
		
		#Get PPT
		os.chdir(digest)
		
		for myppt in glob.glob('*_ppt.fas'):
			pptseqs = list(SeqIO.parse(myppt, "fasta"))
			for pptseq in pptseqs:
				if pptseq.id==record.id:
					os.chdir(basepath)
					with open('PPTseq_'+base+'.fas','a') as ppt:
						ppt.write(">"+record.id+'\n')
						ppt.write(str(pptseq.seq)+'\n')
		
		#Get 3'LRT
		os.chdir(digest)
		for myltr3 in glob.glob('*_3ltr.fas'):
			ltr3seqs = list(SeqIO.parse(myltr3, "fasta"))
			for ltr3seq in ltr3seqs:
				if ltr3seq.id==record.id:
					os.chdir(basepath)
					with open('ltr3seq_'+base+'.fas','a') as ltr3:
						ltr3.write(">"+record.id+'_'+base+'\n')
						ltr3.write(str(ltr3seq.seq)+'\n')

		#Get 5'LRT
		os.chdir(digest)
		for myltr5 in glob.glob('*_5ltr.fas'):
			ltr5seqs = list(SeqIO.parse(myltr5, "fasta"))
			for ltr5seq in ltr5seqs:
				if ltr5seq.id==record.id:
					os.chdir(basepath)
					with open('ltr5seq_'+base+'.fas','a') as ltr5:
						ltr5.write(">"+record.id+'_'+base+'\n')
						ltr5.write(str(ltr5seq.seq)+'\n')
		os.chdir(basepath)
		
		#get similarity
		sim=open('similarity_'+base+'.txt','a') 
		for rec in db.all_features(limit,featuretype='LTR_retrotransposon'):
			similarity=rec.attributes['ltr_similarity']
			similarity = float(*similarity)
			sim.write(record.id+'\t'+str(similarity)+'\n')
		
		'''
		chrom=re.sub(r'(.*)_\d+_\d+', r'\1', record.id.rstrip())
		c=0
		start=0
		end=0
		parent=rec_dict[record.id.rstrip()]
		#print record.id
		
		for rec in db.children(parent, featuretype='long_terminal_repeat',order_by='start'):
			#print rec 
			if c==0:
				start=rec.end-1
				c=c+1
			else:
				end=rec.start
				c=c+1
			#print start, end
			
			if (c==2):
				with open('internal_'+base+'.bed','a') as internal:
					internal.write(chrom+'\t'+str(start)+'\t'+str(end)+'\t'+record.id+'\n')
		
		'''
		chrom=re.sub(r'(.*)_\d+_\d+', r'\1', record.id.rstrip())
		c=0
		start=0
		end=0
		parent=rec_dict[record.id.rstrip()]
		print record.id
		
		for rec in db.children(parent, featuretype='protein_match'):
			

			 

			name=str(*rec.attributes['name'])
		
			dombase=re.split("_",name)[0]
			score=float(rec.score)
			#print dombase
			if dombase=="RT" or dombase=="rvt" or dombase=="RVT":
				print dombase
				if my_score["RT"]>score:
					
					my_score["RT"]=rec.score
					my_type["RT"]=name
					my_start["RT"]=int(rec.start)-800-1
					my_end["RT"]=int(rec.stop)+800
					my_strand["RT"]=rec.strand
		os.chdir(basepath)

		if my_type["RT"]!='':
			with open('RT800EV_'+base+'.bed','a') as RT:
					RT.write(chrom+'\t'+str(my_start["RT"])+'\t'+str(my_end["RT"])+'\t'+my_strand["RT"]+'\t'+record.id+'\n')
			'''
		
	# Move cluster file to its folder
	os.chdir(savedPath)
	#shutil.copy(myfasta, basepath)
if __name__ == "__main__":
	main(sys.argv[1:])

