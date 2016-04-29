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

participants = pd.DataFrame.from_csv('participants.csv', index_col=None)
with file('certificate.tex') as fid:
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
subprocess.call(['pdfjoin', '-o', 'certificates.pdf'] + all_pdfs)
