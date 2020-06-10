#!/usr/bin/env python

from __future__ import division
import sys
import math

word_hits={}  ##store all word as key and list all docs contaiing the word as value


##Inerse_index dictionary:For all word in all document, key is doc and value(another dictionary) is each word in the doc along with their frequecy, tf, idf, tf_idf
##e.g., inverse_index={"doc1":{"word":[hits,freq,tf,tf_idf]}}

inverse_index={}

for line in sys.stdin:
	word_file, count = line.strip().split("\t", 1)
	word, doc = word_file.split("_")
	
	try:
		count = int(count)
	except ValueError:
        	continue
	
	if word not in word_hits:
		doc_list=[]
		doc_list.append(doc)  #which doc has the word, add it to the list
		word_hits[word] = [count,doc_list]
	else:
		current_count = word_hits[word][0]
		current_doc_list=[]
		current_doc_list = word_hits[word][1]
		if doc not in current_doc_list:
			current_doc_list.append(doc)
        	word_hits[word] = [current_count+1, current_doc_list]

	if doc not in inverse_index:
		word_dict={}
		word_list=[0,1,0,0]
		
		word_dict[word]=word_list
		
		inverse_index[doc]=word_dict 

	else:
		word_dict={}
		word_dict=inverse_index[doc]
		
		word_list=[0,1,0,0]
		
		if word not in word_dict:
			word_dict[word]=word_list
		else:
			current_doc_count=word_dict[word][1]
			word_dict[word]=[0,current_doc_count+1,0,0]
		inverse_index[doc]=word_dict  ##Add inner_doc_dict to doc key as value
				
print '\n\n----Inverse Index-----\n\n'

for word,count_doc_list in word_hits.items():
	print '%s\t%s\t%s\n' %(word, count_doc_list[0], str(count_doc_list[1]))


print '\n\n----TF-IDF RELEVENCE SCORE---\n\n'

for doc,doc_dict in inverse_index.items():
	print '\n%s\t%s\t%s\t%s\t\t%s\t\t%s' %(doc,'HITS','FREQ','TF','IDF','TF-IDF')
	
	N=len(inverse_index) ##Number of documents in the directory
	
	##GET Total Word in each document
        total_word_per_doc=0
        for word_count in doc_dict.values():
                total_word_per_doc+=word_count[1]

	##for each word in a doc
	for word_key,word_value_list in doc_dict.items():

		#hits: How many doc contain the word
                hits=len(word_hits[word_key][1])

		#frequency: how many times a word appear in a doc
                frequency=word_value_list[1]

		#tf: frequency: how many times a word appear in a doc/total_word_per_doc
                tf=frequency/total_word_per_doc

		#idf: log(total number of docs/hits: how many doc contain the word))
                idf=math.log10(N/hits)

		#tf_idf: Term Frequecy (TF) * idf
                tf_idf=tf*idf

		print '%s\t%s\t%s\t%s\t%s\t%s' % (word_key,hits,frequency,tf,idf,tf_idf)
