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


def combine_description_comments(filename, outfile):
    """
    input: filename, the file which store the crawled data; 
    outfile: the file contain description and comments
    example:bug_id  description comments
    """
    output = open(outfile, 'w')
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split("\t")
            if len(mid) == 15:
                bug_id = mid[0]
                desc = mid[12]
                comm = mid[13]
                output.write(bug_id)
                output.write('\t')
                output.write(desc)
                output.write(' ')
                output.write(comm)
                output.write('\n')
    output.close()


def copyfile(srcfile, dstfile, linenum):
    """
    get linenum different lines out from srcfile at random and write them into dstfile
    srcfile:bug_id  description comments
    dsffile:bug_id  description comments
    """
    result = []
    ret = False
    try:
        srcfd = open(srcfile, 'r')
    except IOError:
        print 'srcfile doesnot exist!'
        return ret
    try:
        dstfd = open(dstfile, 'w')
    except IOError:
        print 'dstfile doesnot exist!'
        return ret
    srclines = srcfd.readlines()
    srclen = len(srclines)
    while len(Set(result)) < srclen and len(Set(result)) < int(linenum):
        s = random.randint(0, srclen - 1)
        result.append(srclines[s])
    for content in Set(result):
        dstfd.write(content)
    srcfd.close()
    dstfd.close()
    ret = True
    return ret


def preProcess(filename, processed_file):
    output = open(processed_file, 'w')
    english_stopwords = stopwords.words('english')
    #english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    st = LancasterStemmer()
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split('\t')
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
                output.write(mid[0])
                output.write('\t')
                for word in processed_words:
                    output.write(word)
                    output.write(' ')
                output.write('\n')
    output.close()

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

def compute_token_times(filename, outfile):
    output = open(outfile, 'w')
    token_times = {}
    with open(filename) as of:
        for line in of:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 2:
                content = mid[1].strip()
                words = content.split()
                for word in words:
                    word = word.strip()
                    if hasNumbers(word):
                        continue
                    if word not in token_times:
                        token_times[word] = 0
                    token_times[word] = token_times[word] + 1
    for key in token_times:
        output.write(key)
        output.write(':')
        output.write(str(token_times[key]))
        output.write('\n')
    output.close()
    return token_times


def main():
    """
    main function
    """
    linenum = 4000
    filename = "/home/carrie/scrapyCrawe/Eclipse_bugReport/nonreopen_Eclipse_Tools_1.txt"
    srcfile = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/nonreopen_description_comments.txt"
    dstfile = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/corpus_nonreopen.txt"
    processed_file = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/processed_corpus_nonreopen.txt"
    maps_file = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/nonreopen_token_times.txt"
    combine_description_comments(filename, srcfile)
    copyfile(srcfile, dstfile, linenum)
    preProcess(dstfile, processed_file)
    compute_token_times(processed_file, maps_file)


if __name__ == "__main__":
    main()
