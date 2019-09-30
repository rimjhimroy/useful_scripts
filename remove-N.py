import sys
import re
import textwrap
seq=""
header=""

for l in open(sys.argv[1]):
    l=l.rstrip("\n")
    if l.startswith(">"):
        header=l
    else:
        l=re.sub("N","",l)
        seq+=l


print header
cp=0
while cp<len(seq):
    print seq[cp:cp+50]
    cp+=50
