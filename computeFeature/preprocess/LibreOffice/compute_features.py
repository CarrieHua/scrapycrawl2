#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file compute_features.py
# * @author Carrie
# * @date 2017/01/13
# * @brief acquire each feature in need 
# **
"""

import os
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import datetime
from dateutil import parser
from compute_combined_probability import compute_fifteen_token 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def token_probability(token_probability_file):
    token_probability_dict = {}
    with open(token_probability_file) as f:
        for line in f:
            line = line.strip()
            mid = line.split(':')
            token_probability_dict[mid[0]] = mid[1]
    return token_probability_dict


def compute_Bayesian_score(text, token_probability_dict):
    content=''
    for token in text:
        content = content + ' ' + token
    if content.strip():
        probs = compute_fifteen_token(token_probability_dict, content.strip())
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
    else:
        score = 0.5
    return score


def is_leap_year(year):
    if (((year % 100 == 0) and (year % 400 == 0)) or ((year % 100 != 0) and (year % 4 == 0))):
        return True
    else:
        return False


def get_week_day(date):
    week_day = {0:'Monday', 1:'Tuesday', 2:'Wednesday',3:'Thursday',4:'Friday', 5:'Saturday', 6:'Sunday'}
    day = date.weekday()
    return week_day[day]


def compute_day_of_year(date):
    mid = date.strip().split('-')
    not_leap_year = {1:31,2:28,3:31,4:20,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    leap_year = {1:31,2:29,3:31,4:20,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    year = mid[0]
    month = mid[1]
    month_day = mid[2]
    day_of_year = 0
    if is_leap_year(int(year)):
        i = 1
        while i < int(month):
            day_of_year += leap_year[i]
            i = i + 1
            day_of_year += int(month_day)
    else:
        i = 1
        while i < int(month):
            day_of_year += not_leap_year[i]
            i = i + 1
            day_of_year += int(month_day)
    return day_of_year

def distance_between_days(date1, date2):
    date1 = parser.parse(date1)
    date2 = parser.parse(date2)
    return (date2 - date1).days

def compute_time(hour):
    time = ''
    if int(hour) >= 7 and int(hour) <= 12:
        time = 'morning'
    elif int(hour) > 12 and int(hour) <= 17:
        time = 'afternoon'
    elif int(hour) > 17 and int(hour) <= 24:
        time = 'evening'
    elif int(hour) > 0 and int(hour) < 7:
        time = 'night'
    return time

def compute_weekday(modified_time):
    mid = modified_time.split()
    date = mid[0] + ' ' + mid[1]
    date = parser.parse(date)
    weekday = get_week_day(date)
    return weekday
def compute_features(filename, token_probability_dict, outfile):
    """
    filename: the file which contains bug report from bugzilla,eg nonreopen_Mozilla_1.txt
    outfil: the file which contains work habits features
    """
    reporters_dict = compute_reporter_dict(filename)
    fixers_dict = compute_fixer_dict(filename)
    output = open(outfile, 'w')
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 22:
                #bug_id
                output.write(mid[0])
                output.write('\t')
                modified_time = mid[11].strip()
                #compute time
                hour = modified_time.split()[1].split(':')[0]
                time = compute_time(hour)
                output.write(time)
                output.write('\t')
                #compute Month day
                month_day = modified_time.split()[0].split('-')[-1]
                output.write(month_day)
                output.write('\t')
                #compute Month
                month = modified_time.split('-')[1]
                output.write(month)
                output.write('\t')
                #compute Day of year
                day_of_year = compute_day_of_year(modified_time.split()[0])
                output.write(str(day_of_year))
                output.write('\t')
                #compute Weekday
                weekday = compute_weekday(modified_time)
                output.write(weekday)
                output.write('\t')
                #compute alias
                alias = mid[2].strip()
                output.write(alias)
                output.write('\t')
                #compute product
                product = mid[3].strip()
                output.write(product)
                output.write('\t')
                #compute component
                component = mid[4].strip()
                output.write(component)
                output.write('\t')
                #compute version
                version = mid[5].strip()
                output.write(version)
                output.write('\t')
                #compute hardware
                hardware = mid[6].strip()
                output.write(hardware)
                output.write('\t')
                #compute importance which contains severity and priority
                importance = mid[7].split()
                priority = importance[0]
                severity = importance[1]
                output.write(priority)
                output.write('\t')
                output.write(severity)
                output.write('\t')
                #compute assignee
                assignee = mid[8].strip()
                output.write(assignee)
                output.write('\t')
                #compute CC
                cc = mid[12].strip().split()[0]
                output.write(cc)
                output.write('\t')
                #compute description size
                description = mid[13].strip()
                preProcessed_desc = preProcess(description)
                desc_size = len(preProcessed_desc)
                output.write(str(desc_size))
                output.write('\t')
                #compute description bayesian score
                desc_score = compute_Bayesian_score(preProcessed_desc, token_probability_dict)
                output.write(str(desc_score))
                output.write('\t')
                #compute comments size
                comments = mid[14].strip()
                preProcessed_comms = preProcess(comments)
                comms_size = len(preProcessed_comms)
                output.write(str(comms_size))
                output.write('\t')
                #compute comments bayesian score
                comms_score = compute_Bayesian_score(preProcessed_comms, token_probability_dict)
                output.write(str(comms_score))
                output.write('\t')
                #compute the number of comments
                num_comments = mid[15].strip()
                output.write(num_comments)
                output.write('\t')
                #compute priority changed
                priority_changed = mid[18]
                output.write(priority_changed)
                output.write('\t')
                #compute severity changed
                severity_changed = mid[19]
                output.write(severity_changed)
                output.write('\t')
                #compute time days
                date1 = mid[9].strip().split()[0]
                date2 = mid[11].strip().split()[0]
                time_days = distance_between_days(date1, date2)
                output.write(str(time_days))
                output.write('\t')
                #compute last status
                status_resolution = mid[1].strip().split()
                if len(status_resolution) == 1:
                    output.write(status_resolution[0])
                    output.write('\t')
                    output.write('--')
                    output.write('\t')
                else:
                    status = status_resolution[0]
                    resolution = status_resolution[1]
                    output.write(status)
                    output.write('\t')
                    output.write(resolution)
                    output.write('\t')
                #compute the number times of fix
                num_fix = mid[17]
                output.write(num_fix)
                output.write('\t')
                #compute reporter
                reporter = mid[10]
                output.write(reporter)
                output.write('\t')
                #compute fixer
                fixer = mid[20]
                output.write(fixer)
                output.write('\t')
                #compute reporter experience
                time1 = mid[9].split()
                reported_time = time1[0] + ' ' + time1[1]
                reporter_experience = compute_reporter_experience(reporter, reported_time, reporters_dict)
                output.write(str(reporter_experience))
                output.write('\t')
                #compute fixer experience
                time2 = mid[11].split()
                fixer_time = time2[0] + ' ' + time2[1]
                fixer_experience = compute_fixer_experience(fixer, fixer_time, fixers_dict)
                output.write(str(fixer_experience))
                output.write('\t')
                #remod
                output.write(mid[21])
                output.write('\n')



def preProcess(content):
    english_stopwords = stopwords.words('english')
    st = LancasterStemmer()
    content = content.strip()
    content = unicode(content, errors='ignore')
    #lower the words
    content = content.lower()
    words = nltk.word_tokenize(content)
    processed_words = []
    for word in words:
        if word not in english_stopwords:
            w = word.replace(string.punctuation, "")
            processed_words.append(st.stem(w))
    return processed_words

def compute_reporter_dict(filename):
    """
    filename:the file which contains all the fixer in the project
    """
    # a dict which represents reporter_name:[time1, time2 ,...]
    reporters_dict = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split("\t")
            if len(mid) == 22:
                name = mid[10]
                reported_time = mid[9].split()
                time = reported_time[0] + ' ' + reported_time[1]
                if name not in reporters_dict:
                    reporters_dict[name] = []
                reporters_dict[name].append(time)
    return reporters_dict


def compute_fixer_dict(filename):
    """
    filename:the file which contains all the fixer in the project
    """
    # a dict which represents fixer_name:[time1, time2 ,...]
    fixers_dict = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split("\t")
            if len(mid) == 22:
                name = mid[20]
                modified_time = mid[11].split()
                time = modified_time[0] + ' ' + modified_time[1]
                if name not in fixers_dict:
                    fixers_dict[name] = []
                fixers_dict[name].append(time)
    return fixers_dict

def compute_reporter_experience(reporter, time, reporters_dict):
    reporters_dict[reporter].sort()
    count = 0
    for t in reporters_dict[reporter]:
        if t <= time:
            count = count + 1
        else:
            break
    return count

def compute_fixer_experience(fixer, time, fixers_dict):
    """
    input: fixer which needs compute the experience; 
    """
    fixers_dict[fixer].sort()
    count = 0
    for t in fixers_dict[fixer]:
        if t <= time:
            count = count + 1
        else:
            break
    return count


def main():
    """
    main function
    """
    filename = "/home/carrie/scrapyCrawe/OpenOffice_bugReport/OpenOffice.txt"
    features_file = "/home/carrie/scrapyCrawe/computeFeature/OpenOffice/OpenOffice_features.txt"
    token_probability_file = "/home/carrie/scrapyCrawe/computeFeature/OpenOffice/token_probability.txt"
    token_probability_dict = token_probability(token_probability_file)
    compute_features(filename, token_probability_dict, features_file)


if __name__ == "__main__":
    main()
