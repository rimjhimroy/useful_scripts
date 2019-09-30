#!/usr/bin/awk -f
# Use after sorting with: sort -k1,1 -k4,4n -k5,5n -k6,6n file.gff
# It gives a list of nested elements in your input gff
# getNestedElements.awk input.gff output.nested.elements.gff
# Use the output to clean remove nested elements from your gff
# grep -v -x -f output.of.this.script gfffile.toremove.nested.from > cleaned.gff
{
    if (NR > 1) {
        currentChr = $1
        currentStart = $4
        currentStop = $5
        currentScore = $6
        currentLen = currentStop - currentStart
        if ((previousChr == currentChr) && (previousStart == currentStart) && (previousStop == currentStop) && (previousScore>currentScore)) {
            print $0;
        }
        else if ((previousChr == currentChr) && (previousStart <= currentStart) && (previousStop >= currentStop)) {
            print $0;
        }
        else {
            previousChr = currentChr
            previousStart = currentStart
            previousStop = currentStop
        }
    }
    else {
        previousChr = $1
        previousStart = $4
        previousStop = $5
        previousScore = $6
        previousLen = previousStop - previousStart
    }
}
