#!/usr/bin/env python
#coding=utf-8

import pandas as pd

df = pd.DataFrame.from_csv('data/post_survey.csv')
columns = zip(df.columns, ['single-choice'] * len(df.columns))

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

