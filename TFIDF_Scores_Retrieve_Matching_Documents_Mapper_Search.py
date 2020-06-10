#!/usr/bin/python

import os
import sys

# Read pairs as lines of input from STDIN
for line in sys.stdin:
	line = line.strip()
	words = line.split()
	for word in words:
		try:
			filename = os.environ['mapreduce_map_input_file'] ##Get the input filename
		except KeyError:
			filename = os.environ['map_input_file']
		word_file = word + "_" + filename[-7:-4] #remove last 4 char .txt and take only 100 from /path/100.txt
		#print '%s\t%s\t%s' % (word,1,filename)
		print ("%s\t%s" %( word_file, 1))
