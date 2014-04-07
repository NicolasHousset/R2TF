# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 09:50:21 2014

@author: compomics
"""

from pandas import DataFrame, read_csv
import pandas as pd
import re

# We start with one project
projNumber = 2000
Location = "/mnt/compomics/Nicolas/Python/R2TF/data/project"+str(projNumber)+".csv"

VarNames = ['Sequence','rtsec','projectid','lcrunid','lcrun.name','spectrumid','instrumentid','protocolid','filecount',
            'creationdate','scanid','number','userid','identified','score','idthreshold','confidence','DB',
            'total_spectrum_intensity','mass_to_charge','charge','accession','start','end']
df = read_csv(Location, names=VarNames, index_col='spectrumid')

# Took me a while to find the right unction...
df_reduced = df[pd.notnull(df['Sequence'].values)]

# An example with a modification
mod_seq = df_reduced['Sequence'][91726693]
new_seq = mod_seq

parser_index = 0
writer_index = 0
pep_length = len(mod_seq)
temp_char = ''
n_term_parsing = True
main_parsing = False
c_term_parsing = False
amino_parsing = True
mod_parsing = False

n_term_re = re.compile(r"\w")
n_term_re2 = re.compile(r"-")
main_term_re = re.compile(r"[A-Z]")
main_term_re2 = re.compile(r"\w")

char_values = []
new_values = []
for i in range(pep_length):
    char_values.append(mod_seq[i])
    new_values.append('')
TransformDataSet = zip(char_values,new_values)
df = DataFrame(data = TransformDataSet, columns=['Old','New'])


while(parser_index <= pep_length):
    if(n_term_parsing):
        if(n_term_re.match(df['Old'][parser_index])):
            df['New'][writer_index] = df['Old'][parser_index]
            parser_index += 1
            writer_index += 1
        elif(n_term_re2.match(df['Old'][parser_index])):
            df['New'][writer_index] = df['Old'][parser_index]
            parser_index += 1
            writer_index += 1
            n_term_parsing = False
            main_parsing = True
            temp_char = df['Old'][parser_index]
    elif(main_parsing):
        if(amino_parsing):
            if(main_term_re.match(temp_char)):
                df['New'][writer_index] = temp_char
                parser_index += 1
                writer_index += 1
                temp_char = df['Old'][parser_index]
            elif(temp_char == "<"):
                amino_parsing = False
                mod_parsing = True
                parser_index += 1
        elif(mod_parsing):
            if(main_term_re2.match(df['Old'][parser_index])):
                df['New'][writer_index] = df['Old'][parser_index].lower()
                parser_index += 1
                writer_index += 1
            elif(df['Old'][parser_index] == ">"):
                amino_parsing = True
                mod_parsing = False
                parser_index += 1
            elif(df['Old'][parser_index] == "*"):
                parser_index += 1
    elif(c_term_parsing):
        pass

