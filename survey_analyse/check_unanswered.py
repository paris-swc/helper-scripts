#!/usr/bin/env python
#coding=utf-8
"""Script to find participants that did not fill in the survey"""

import pandas as pd

remap_emails = { 
        'someone@gmail.com' : 'someone@example.com'
        }

def map_emails(emails):
    remap = pd.Series(remap_emails)
    f = remap[emails.values]
    f[f.isnull()] = emails.values[f.isnull()]
    return f

df_survey = pd.DataFrame.from_csv('data/post_survey.csv')
df_participants = pd.DataFrame.from_csv('data/list_participants.csv', sep=';')

df_participants = df_participants[:29]

students = df_participants['MAIL']
responses = df_survey['Email address:']
responses = responses.str.strip()
students = students.str.strip()

responses = responses.replace(remap_emails)
response_set = set(responses)
student_set = set(students)

non_matched = response_set - student_set
assert not non_matched, 'non-matched emails\n' + "\n".join(non_matched)

missing = student_set - response_set

print("Missing: " + ",".join(missing))

emails_lookup = df_participants.copy()
emails_lookup.columns = emails_lookup.columns.str.lower()
emails_lookup = emails_lookup.set_index('mail')
i = list(missing)
df_missing = emails_lookup.ix[i, ['firstname', 'lastname']]
df_missing.to_csv('missing_responses.csv', index=True)
