#!/usr/bin/env python

from __future__ import division
import sys
import math

word_hits={}  ##store all word as key and list all docs contaiing the word as value


##Inerse_index dictionary:For all word in all document, key is doc and value(another dictionary) is each word in the doc along with their frequecy, tf, idf, tf_idf
##e.g., inverse_index={"doc1":{"word":[hits,freq,tf,tf_idf]}}

inverse_index={}

query="the big data"
topN=3

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
				

##all_tf_idf_dict={"doc1":{"word1":tfidf}}
all_tf_idf_dict={}

for doc,doc_dict in inverse_index.items():
#	print '\n%s\t%s\t%s\t%s\t\t%s\t\t%s' %(doc,'HITS','FREQ','TF','IDF','TF-IDF')
	
	N=len(inverse_index) ##Number of documents in the directory
	
	##GET Total Word in each document
        total_word_per_doc=0
        for word_count in doc_dict.values():
                total_word_per_doc+=word_count[1]
	
	each_doc_dict={}

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
		
		#tf_idf_list=[]
		#tf_idf_list.append(word_key)  #load the word in a doc
		#tf_idf_list.append(tf_idf)    #load tf_idf for the word in a doc
		
		each_doc_dict[word_key]=tf_idf

		#print '%s\t%s\n' % (word_key,each_doc_dict[word_key])
	all_tf_idf_dict[doc] = each_doc_dict


###Print all word and their tf-idf 
#for key,value in all_tf_idf_dict.items():
	#print '%s\t%s\n' %(key,'TF-IDF')
#	for w,tfidf in value.items():
		#print '%s\t%s\n' %(w,tfidf)

##Search

query_word_list=query.split()

score_dict={}

for dd,vv in all_tf_idf_dict.items():
	score_in_doc=0
	score_in_doc_sum=0
	count=0
	for query_word in query_word_list:
		#get_docs_list=word_hits[query_word][1]
		#print '%s\t%s\n' %(query_word,str(get_docs_list))
	
		#for d in get_docs_list:
		if query_word in vv:
			score_in_doc_sum+=float(vv[query_word])
			count+=1
	score_in_doc=score_in_doc_sum*(count/len(query_word_list))		
	score_dict[dd]=score_in_doc

#print "\n\nScore\n\n"

#for dc,sc in score_dict.items():
#	print '%s\t%s' %(dc,str(sc))		

print 'Top %s Matching Document\n\n' %(topN)
print '%s\t\t%s\n' %("DOCNAME","SCORE")

c=0
for key, v2 in sorted(score_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    	if c < topN:
		print '%s\t%s\n' % (key, v2)
	c+=1
