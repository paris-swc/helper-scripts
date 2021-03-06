#!/usr/bin/env python
#coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import jinja2
import tempfile
import subprocess
import shutil
import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('participants', help='CSV file with participants')
parser.add_argument('--template', '-t', default='certificate.tex', help='LaTeX certificate template')

args = parser.parse_args()

participants = pd.DataFrame.from_csv(args.participants, index_col=None)
with file(args.template) as fid:
    t = jinja2.Template(fid.read().decode('utf-8'))

tmpdir = tempfile.mkdtemp()
shutil.copy('software-carpentry-banner.png', tmpdir)

for pid in range(len(participants)):

    participant = participants.ix[pid]
    name = participant['firstname'] + ' ' + participant['lastname']
    latex_src = t.render(name=name.decode('utf-8'))


    latex_fname = os.path.join(tmpdir, 'participant{}.tex'.format(pid))

    with file(latex_fname, 'w') as latex_file:
        latex_file.write(latex_src.encode('utf-8'))

    fname, ext = os.path.splitext(latex_fname)

    subprocess.call(['xelatex', latex_fname], cwd=tmpdir)
    import glob

    all_pdfs = glob.glob(os.path.join(tmpdir, '*.pdf'))

pdf_filename = os.path.splitext(args.template)[0] + '.pdf'
subprocess.call(['pdfjoin', '-o', pdf_filename] + all_pdfs)
