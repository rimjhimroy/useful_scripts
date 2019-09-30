from blast import parse

fh = open('test.outfmt6')
for blast_record in parse(fh):
    print('query id: {}'.format(blast_record.qid))
    for hit in blast_record.hits:
        for hsp in hit:
            print('****Alignment****')
            print('sequence:', hsp.sid)
            print('length:', hsp.length)
            print('e value:', hsp.evalue)
fh.close()
