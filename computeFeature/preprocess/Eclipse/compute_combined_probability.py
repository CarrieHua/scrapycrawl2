#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file compute_combined_probability.py
# * @author Carrie
# * @date 2017/01/13
# * @brief calculate the probability that a bug will reopen 
# **
"""

import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from combine_description_comments import hasNumbers
from combine_description_comments import preProcess


def extract_description(filename, desc_file):
    output = open(desc_file, 'w')
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 16:
                bug_id = mid[0]
                desc = mid[13]
                output.write(bug_id)
                output.write('\t')
                output.write(desc)
                output.write('\n')
    output.close()


def extract_comments(filename, comms_file):
    output = open(comms_file, 'w')
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 16:
                bug_id = mid[0]
                comm = mid[14]
                output.write(bug_id)
                output.write('\t')
                output.write(comm)
                output.write('\n')
    output.close()

def compute_combined_prob(filename, third_dictfile, outfile):
    third_dict = {}
    output = open(outfile, 'w')
    with open(third_dictfile) as f:
        for line in f:
            line = line.strip()
            mid = line.split(':')
            third_dict[mid[0]] = mid[1]
    with open(filename) as of:
        for line in of:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 1:
                output.write(mid[0])
                output.write('\t')
                output.write(str(0.5))
                output.write('\n')
            if len(mid) == 2:
                probs = compute_fifteen_token(third_dict, mid[1])
                prod = 1
                for prob in probs:
                    prod = prod * float(prob)
                index = 0
                while index < len(probs):
                    probs[index] = 1 - float(probs[index])
                    index = index + 1
                a = 1
                for prob in probs:
                    a = a * float(prob)
                b = prod + a
                score = prod / b
                output.write(mid[0])
                output.write('\t')
                output.write(str(score))
                output.write('\n')
    output.close()

def compute_fifteen_token(third_dict, text):
    text = text.strip()
    words = text.split()
    token_prob = {}
    for word in words:
        word = word.strip()
        if hasNumbers(word):
            continue
        if word not in third_dict:
            token_prob[word] = 0.4
        else:
            token_prob[word] = third_dict[word]
    dict_for_sort = {}
    for key in token_prob:
        dict_for_sort[key] = abs(float(token_prob[key]) - 0.5)
    sorted_token_probs = sorted(dict_for_sort.items(), key = lambda item:item[1], reverse=True)
    probs = []
    i = 0
    while i < len(token_prob) and i < 15:
        probs.append(token_prob[sorted_token_probs[i][0]])
        i = i + 1
    return probs


def main():
    """
    main function
    """
    filename = "/home/carrie/scrapyCrawe/bugReport/nonReopen_Firefox_1.txt"
    desc_file = "/home/carrie/scrapyCrawe/computeFeature/Firefox/nonreopen_description.txt"
    processed_desc_file = "/home/carrie/scrapyCrawe/computeFeature/Firefox/processed_nonreopen_description.txt"
    comms_file = "/home/carrie/scrapyCrawe/computeFeature/Firefox/nonreopen_comments.txt"
    processed_comms_file = "/home/carrie/scrapyCrawe/computeFeature/Firefox/processed_nonreopen_comments.txt"
    third_dictfile = "/home/carrie/scrapyCrawe/computeFeature/Firefox/token_probability.txt"
    desc_scorefile = "/home/carrie/scrapyCrawe/computeFeature/Firefox/nonreopen_desc_score.txt"
    comms_scorefile = "/home/carrie/scrapyCrawe/computeFeature/Firefox/nonreopen_comms_score.txt"
    extract_description(filename, desc_file)
    extract_comments(filename, comms_file)
    preProcess(desc_file, processed_desc_file)
    preProcess(comms_file, processed_comms_file)
    compute_combined_prob(processed_desc_file, third_dictfile, desc_scorefile)
    compute_combined_prob(processed_comms_file, third_dictfile, comms_scorefile)

if __name__ == "__main__":
    main()
