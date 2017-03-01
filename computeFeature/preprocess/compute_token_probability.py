#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file create a third hash table which maps each token to the probability that a bug containing it will happen
# * @author Carrie
# * @date 2017/01/13
# * @brief acquire token for its probability of reopen 
# **
"""

import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from combine_description_comments import compute_token_times


def compute_token_probability(reopen_corpus,nonreopen_corpus,reopen_dictfile, nonreopen_dictfile, third_dictfile, reopen_num, nonreopen_num):
    
    dict_reopen = compute_token_times(reopen_corpus, reopen_dictfile)
    dict_nonReopen = compute_token_times(nonreopen_corpus, nonreopen_dictfile)
    dict_third = {}
    output = open(third_dictfile, 'w')
    #the union of tokens which from dict_reopen and dict_nonReopen
    tokens = dict(dict_reopen, **dict_nonReopen)
    for token in tokens:
        if token not in dict_reopen:
            reopen = 0
        else:
            reopen = float(dict_reopen[token])
            #reopen = 2 * float(dict_reopen[token])
        if token not in dict_nonReopen:
            nonreopen = 0
        else:
            nonreopen = float(dict_nonReopen[token])
        if reopen + nonreopen >= 5.0:
            a = min(1, reopen / reopen_num)
            b = min(1, nonreopen / nonreopen_num)
            c = a + b
            d = a / c
            e = min(0.99, d)
            f = max(0.01, e)
            dict_third[token] = f
            output.write(token)
            output.write(':')
            output.write(str(f))
            output.write('\n')
    output.close()
def main():
    """
    main function
    """
    reopen_corpus = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/processed_corpus_reopen.txt"
    nonreopen_corpus = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/processed_corpus_nonreopen.txt"
    reopen_dictfile = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/reopen_token_times.txt"
    nonreopen_dictfile = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/nonreopen_token_times.txt"
    third_dictfile = "/home/carrie/scrapyCrawe/computeFeature/Eclipse_Tools/token_probability.txt"
    reopen_num = 340
    nonreopen_num = 4000
    compute_token_probability(reopen_corpus,nonreopen_corpus,reopen_dictfile, nonreopen_dictfile, third_dictfile, reopen_num, nonreopen_num)


if __name__ == "__main__":
    main()
