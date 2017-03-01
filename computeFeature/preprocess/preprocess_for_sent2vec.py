#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file combine_description_comments.py
# * @author Carrie
# * @date 2017/01/13
# * @brief acquire the combination of description and comments which will act corpus for computing the times of each token in the corpus
# **
"""

import os
import string
import random
from sets import Set
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def preProcess(filename, processed_file):
    output = open(processed_file, 'w')
    english_stopwords = stopwords.words('english')
    #english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    st = LancasterStemmer()
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 1:
                output.write(' ')
                output.write('\n')
            if len(mid) == 2:
                content = mid[1].strip()
                content = unicode(content, errors='ignore')
                #lower the words
                content = content.lower()
                words = nltk.word_tokenize(content)
                processed_words = []
                for word in words:
                    if word not in english_stopwords:
                        w = word.replace(string.punctuation, "")
                        processed_words.append(st.stem(w))
                #output.write(mid[0])
                #output.write('\t')
                for word in processed_words:
                    output.write(word)
                    output.write(' ')
                output.write('\n')
    output.close()

def main():
    """
    main function
    """
    filename = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/Eclipse_Tools_description_comments.txt"
    processed_file = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/processed_Eclipse_Tools_description_comments.txt"
    preProcess(filename, processed_file)


if __name__ == "__main__":
    main()
