import re
import sys, getopt, os

import multiprocessing as mp

def split_seq(seq, num_pieces):
    # Splits a list into pieces
    start = 0
    for i in xrange(num_pieces):
        stop = start + len(seq[i::num_pieces])
        yield seq[start:stop]
        start = stop   

def replace_all (target,find,replace):
	return replace.join(target.split(find))

def detect_active_keys(keys, data, queue):
    # This function MUST be at the top-level, or
    # it can't be pickled (multiprocessing using pickling)
    queue.put([k for k in keys if k in data])

def mass_replace(data, mappings):
    manager = mp.Manager()
    queue = mp.Queue()
    # Data will be SHARED (not duplicated for each process)
    d = manager.list(data) 

    # Split the MAPPINGS KEYS up into multiple LISTS, 
    # same number as CPUs
    key_batches = split_seq(mappings.keys(), mp.cpu_count())

    # Start the key detections
    processes = []
    for i, keys in enumerate(key_batches):
        p = mp.Process(target=detect_active_keys, args=(keys, d, queue))
        # This is non-blocking
        p.start()
        processes.append(p)

    # Consume the output from the queues
    active_keys = []
    for p in processes:
        # We expect one result per process exactly
        # (this is blocking)
        active_keys.append(queue.get())

    # Wait for the processes to finish
    for p in processes:
        # Note that you MUST only call join() after
        # calling queue.get()
        p.join()

    # Same as original submission, now with MUCH fewer keys
    for key in active_keys:
        data = data.replace(key, mappings[key])

    return data

if __name__ == '__main__':
    # You MUST call the mass_replace function from
    # here, due to how multiprocessing works
	word_list = ''
	filename = ''


	try:
		opts, args = getopt.getopt(sys.argv[1:], 'l:f:', ['word_list=', 'filename='])
	except getopt.GetoptError:
		print "Error"
		print 'replace_word_using_list.py -l <word_list> -f <filename>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'replace_word_using_list.py -l <word_list> -f <filename>'
			sys.exit()
		elif opt in ("-l", "--word_list"):
			word_list = arg
		elif opt in ("-f", "--filename"):
			filename = arg
	print 'list file is "', word_list
	print 'input file is "', filename
	old_new = [i.strip().split('\t') for i in open(word_list)]


	with open("replaced.txt", 'w') as outfile, open(filename) as infile:
		for line in infile:
			for oldnew in old_new:
				if len(oldnew)<2:
					print oldnew
					continue
				#print oldnew[0]
				line = line.replace(oldnew[0],oldnew[1])
			outfile.write(line)

'''
	with open(word_list, 'r') as document:
		mappings = {}
		for line in document:
			line = line.split()
			if not line:  # empty line?
				continue
			mappings[line[0]] = line[1:]
'''

'''
	with open(filename, 'r') as file:
		for line in file:
			print line
			for word, replacement in mappings.items():
				#print word, str(replacement)
				data=replace_all(str(line), word, str(replacement))
		uniqlines = set(data)
		rFile.write(data)
		file.seek(0)

	with open(filename, 'r') as f:
		data = mass_replace(f.read(), mappings)
		f.seek(0)
		f.truncate()
		rFile.write(data)
'''
