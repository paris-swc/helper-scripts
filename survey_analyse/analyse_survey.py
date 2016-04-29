#!/usr/bin/env python
#coding=utf-8

import pandas as pd

columns = [
("What is your career stage?", 'single-choice'),
("What is your discipline?", "multiple-choice"),
("What OS will you use on the laptop you bring to the workshop?", "single-choice"),
("With which programming languages, if any, could you write a program from scratch which imports some data and calculates mean and standard deviation of that data?", "multiple-choice"),
("What best describes how often you currently program?", "single-choice"),
("What best describes the complexity of your programming? (Choose all that apply.)", "multiple-choice"),
("A tab-delimited file has two columns showing the date and the highest temperature on that day. Write a program to produce a graph showing the average highest temperature for each month.", "single-choice"),
("How familiar are you with Git version control?", "single-choice"),
("Consider this task: given the URL for a project on GitHub, check out a working copy of that project, add a file called notes.txt, and commit the change.", "single-choice"),
("How familiar are you with unit testing and code coverage?", "single-choice"),
("Consider this task: given a 200-line function to test, write half a dozen tests using a unit testing framework and use code coverage to check that they exercise every line of the function.", "single-choice"),
("How familiar are you with SQL?", "single-choice"),
("Consider this task: a database has two tables: Scientist and Lab. Scientist's columns are the scientist's user ID, name, and email address; Lab's columns are lab IDs, lab names, and scientist IDs. Write an SQL statement that outputs the number of scientists in each lab.", "single-choice"),
("How familiar do you think you are with the command line?", "single-choice"),
('How would you solve this problem: A directory contains 1000 text files. Create a list of all files that contain the word "Drosophila" and save the result to a file called results.txt.', "single-choice"),
('''Consider the extent to which the following statement applies to you: "Setbacks don't discourage me."''', "single-choice"),
('''Consider the extent to which the following statement applies to you: "I often set a goal but later choose to pursue a different one."''', "single-choice"),
("In three sentences or fewer, describe a common scenario in your daily work in which stronger computing skills would improve your workflow and make you more productive. ", "free"),
("In three sentences or less, please describe your current field of work or your research question.", "free")
]


import sys

fname = sys.argv[1]

df = pd.DataFrame.from_csv(fname)

df.fillna('no answer', inplace=True)
df["What is your discipline?"] = df["What is your discipline?"].str.replace('biology, genetics', 'biology/genetics')

counts = []

for col, question_type in columns:
    if question_type == 'single-choice':
        counts.append(df.groupby(col).size())
    elif question_type == 'multiple-choice':
        all_replies = reduce(lambda x,y: x+y, list(df[col].str.split(',\s*')), [])
        mc_df = pd.DataFrame(all_replies)
        counts.append(mc_df.groupby(0).size())
    elif question_type == 'free':
        counts.append(list(df[col].sort(inplace=False)))



for (c, _), responses in zip(columns, counts):
    print c
    if isinstance(responses, pd.Series):
        for r, freq in responses.iteritems():
            print '*', r,':', freq
    else:
        for r in responses:
            print "*", r.strip()

    print

