#!/usr/bin/python3

import sys, os

sep = '\t'

# We open STDIN and STDOUT
with sys.stdin as fin:
    with sys.stdout as fout:
    
        # For every line in STDIN
        for line in fin:
        
            # Strip off leading and trailing whitespace
            line = line.strip()
            
            # We split the line into word tokens. Use whitespace to split.
            # Note we don't deal with punctuation.
            
            word = line.split(",")[16] # Origin is the 17th column

            fout.write("{0}{1}1\n".format(word, sep))