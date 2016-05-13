# -*- coding: utf-8 -*-
####################### MERGE WITH ANEWAPI ########################

#!/usr/bin/env python
# encoding: utf-8
"""
Requires NLTK 
Requires the presence of the file "sent_dict.csv" in this directory

This module defines two functions, which calculates the mood of a text:

mood_value = anewize_string( string )
mood_value = anewize_list( list_of_strings ) # e.g output of nltk's "tokenize"

"""

import sys
import os
from nltk import *
import nltk
import math
import numpy
import codecs
#import matplotlib.pyplot as plt


# define anew dictionary
anew_dict = {}

# import the anew set
f = codecs.open('/Users/Maxim/Documents/Imperial Data Science Society/Twitter_analysis/sent_dict.csv','r','utf8')
f.readline()
for line in f:
    #word,wno,val,valsd,aro,arosd,dom,domsd,freq = line.rstrip().split(',')
    l = line.rstrip().split(',')
    i,word,v_mean_sum,v_sd_sum,v_rat_sum,a_mean_sum,a_sd_sum,a_rat_sum,d_mean_sum,d_sd_sum,d_rat_sum,v_mean_m,v_sd_m,v_rat_m,v_mean_f,v_sd_f,v_rat_f,a_mean_m,a_sd_m,a_rat_m,a_mean_f,a_sd_f,a_rat_f,d_mean_m,d_sd_m,d_rat_m,d_mean_f,d_sd_f,d_rat_f,v_mean_y,v_sd_y,v_rat_y,v_mean_o,v_sd_o,v_rat_o,a_mean_y,a_sd_y,a_rat_y,a_mean_o,a_sd_o,a_rat_o,d_mean_y,d_sd_y,d_rat_y,d_mean_o,d_sd_o,d_rat_o,v_mean_l,v_sd_l,v_rat_l,v_mean_h,v_sd_h,v_rat_h,a_mean_l,a_sd_l,a_rat_l,a_mean_h,a_sd_h,a_rat_h,d_mean_l,d_sd_l,d_rat_l,d_mean_h,d_sd_h,d_rat_h = l
    #print(line)
    anew_dict[word] = (int(i),float(v_mean_sum),float(v_sd_sum))
f.close()

anew_dict[anew_dict.keys()[1]]


def anewize_string(str):
    values = []
    tokens = nltk.word_tokenize(str)
    anew_words = set( anew_dict.keys() )
    for tt in tokens:
        if tt.isalpha():
            if tt in anew_words:
                values.append(anew_dict[tt])
            
    if len(values) > 0:
        anew_mean = float(sum(values))/float(len(values))
    else:
        anew_mean = 'Null'
    
    return anew_mean

def anewize_list(lst):
    values = []
    tokens = lst
    anew_words = set( anew_dict.keys() )
    for tt in tokens:
        if tt.isalpha():
            if tt in anew_words:
                values.append(anew_dict[tt])

    if len(values) > 0:
        anew_mean = float(sum(values))/float(len(values))
    else:
        anew_mean = 'Null'
    
    return anew_mean


# valence = [1,2,3,4,5,6,7,8,9]
# vCount =  [0,0,0,0,0,0,0,0,0]
# #f = open('/Users/Maxim/Downloads/nltk-2.0b9/anew_all.txt', 'r')
# lines = f.readlines()
# for line in lines:
#     err = '.'
#     l = line.split()
#     j = int(math.floor(float(l[2])))-1
#     if l[8] != err:
#         tru = int(l[8])
#         vCount[j] += tru
# f.close()
# p1 = plt.bar(valence,vCount,1)
# plt.ylabel('Weighted frequency f')
# plt.xlabel('Valence v')


####################### Compute Sentiment ########################
import urllib, urllib2
import datetime
import nltk
import time
from compSent import compSent
from tweet_cleanup import cleanup

try:
    import json
except ImportError:
        import simplejson as json

tdict = []


    tweets = json.load(f)
    #for tweet in tweets:
    #    tweet,_ = cleanup(tweet)
    #    tdict.append(tweet)        
    
tokens = nltk.word_tokenize(tweets[1])

anew_dict['thanks']

test=str(tokens[2])


out=anew_dict[test.lower()]

out[1]

t=tweets[2]
t

x = compSent()

x.compSentiment(t)


        

    



    
