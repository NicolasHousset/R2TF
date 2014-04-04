# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 09:50:21 2014

@author: compomics
"""
import numpy as np
from pandas import DataFrame, read_csv
pd.notnull()
import pandas as pd

# We start with one project
projNumber = 2000
Location = "/mnt/compomics/Nicolas/Python/R2TF/data/project"+str(projNumber)+".csv"

VarNames = ['Sequence','rtsec','projectid','lcrunid','lcrun.name','spectrumid','instrumentid','protocolid','filecount',
            'creationdate','scanid','number','userid','identified','score','idthreshold','confidence','DB',
            'total_spectrum_intensity','mass_to_charge','charge','accession','start','end']
df = read_csv(Location, names=VarNames, index_col='spectrumid')

df.head(5)
mask = df['Sequence'].values != np.nan

pd.notnull(df['Sequence'].values)
df_reduced = df[pd.notnull(df['Sequence'].values)]

'    Nan'.strip(" ")