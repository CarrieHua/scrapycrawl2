#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file combine_features_vec.py
# * @author Carrie
# * @date 2017/01/13
# * @brief combine the features which acquire from bug report and sent2vec of description and comments
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

def combine_features_vec(filename_1,filename_2, features_vec_file, vec_file):
    """
    filename_1:only contains the 24 features from bug report,like Shihab
    filename_2:only contains 100 vec of sentence,eg
                sent0 fea0 fea1.......fea99
    features_vec_file: contain both 24 feature and 100 vec with remod
    vec_file: contain only 100 vec with remod
    """
    output_1 = open(features_vec_file, 'w')
    output_2 = open(vec_file, 'w')
    file_1 = open(filename_1, 'r')
    file_2 = open(filename_2, 'r')
    line_2 = file_2.readline()
    while 1:
        line_1 = file_1.readline()
        line_2 = file_2.readline()
        if not line_1 or not line_2:
            break
        mid_1 = line_1.strip().split('\t')
        mid_2 = line_2.strip().split()
        output_2.write('\t'.join(mid_2[1:]))
        output_2.write('\t')
        output_2.write(mid_1[-1])
        output_2.write('\n')
        output_1.write('\t'.join(mid_2[1:]))
        output_1.write('\t')
        output_1.write('\t'.join(mid_1[1:]))
        output_1.write('\n')
    output_1.close()
    output_2.close()

def main():
    """
    main function
    """
    filename_1 = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/Eclipse_Tools_features.txt"
    filename_2 = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/processed_Eclipse_Tools_sent.txt.vec"
    features_vec_file = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/features_vec.txt"
    vec_file = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/sent_vec.txt"
    combine_features_vec(filename_1,filename_2, features_vec_file, vec_file)


if __name__ == "__main__":
    main()
