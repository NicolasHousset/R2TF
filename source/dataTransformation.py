"""
Created on Fri Mar 28 09:50:21 2014

@author: compomics
"""

import MySQLdb
import pandas.io.sql as psql
from pandas import DataFrame, read_csv
import pandas as pd
import re

def connect_to_mslims(_host, _user, _passwd, _db):
    """A function to connect to the MSLIMS database, returns the cursor"""
    mysql_cn = MySQLdb.connect(host=_host,
                         user=_user,
                         passwd=_passwd,
                         db=_db)
    return mysql_cn


with open('/mnt/compomics/Nicolas/Python/etc/ms_lims.txt','r') as f :
    host = f.readline().strip("\n")
    user = f.readline().strip("\n")
    passwd = f.readline().strip("\n")
    db = f.readline().strip("\n")

con = connect_to_mslims(host,
                      user,
                      passwd,
                      db)

def importProjNumbersFromMSLIMS(_con, _projNumber):
    """A function to extract one project"""
    _test = psql.frame_query("""SELECT projectid FROM project WHERE projectid >= """+
    str(_projNumber), con = _con)
    return _test



# We start with one project
startingProject = 2000
nbProjects = 12

test = importProjNumbersFromMSLIMS(con, startingProject)
VarNames = ['Sequence','rtsec','projectid','lcrunid','lcrun.name','spectrumid','instrumentid','protocolid','filecount',
            'creationdate','scanid','number','userid','identified','score','idthreshold','confidence','DB',
            'total_spectrum_intensity','mass_to_charge','charge','accession','start','end']

for projIndex in range(nbProjects):
    print projIndex
    Location = "/mnt/compomics/Nicolas/Python/R2TF/data/project"+str(test['projectid'][projIndex])+'.csv'
    df = read_csv(Location, names=VarNames, index_col=False)

# Took me a while to find the right function...
    df_reduced = df[pd.notnull(df['Sequence'].values)]
    df_reduced['New_Sequence'] = ""

    for indexing in df_reduced.index:
        mod_seq = df_reduced['Sequence'][indexing]
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


        while(parser_index < pep_length):
            if(n_term_parsing):
                if(df['Old'][parser_index]=='N'):
                    if(df['Old'][parser_index+1]=='H'):
                        if(df['Old'][parser_index+2]=='2'):
                            parser_index += 3
                            df['New'][writer_index] = 'H'
                            writer_index += 1
                elif(n_term_re.match(df['Old'][parser_index])):
                    df['New'][writer_index] = df['Old'][parser_index].lower()
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
                    if(df['Old'][parser_index] == "<"):
                        temp_char = df['Old'][parser_index-1]
                        amino_parsing = False
                        mod_parsing = True
                        parser_index += 1
                        writer_index -= 1
                    elif(main_term_re.match(temp_char)):
                        df['New'][writer_index] = temp_char
                        parser_index += 1
                        writer_index += 1
                        temp_char = df['Old'][parser_index]
                    elif(temp_char == "-"):
                        df['New'][writer_index] = temp_char
                        parser_index += 1
                        writer_index += 1
                        main_parsing = False
                        c_term_parsing = True
                elif(mod_parsing):
                    if(main_term_re2.match(df['Old'][parser_index])):
                        df['New'][writer_index] = df['Old'][parser_index].lower()
                        parser_index += 1
                        writer_index += 1
                    elif(df['Old'][parser_index] == ">"):
                        amino_parsing = True
                        mod_parsing = False
                        parser_index += 1
                        df['New'][writer_index] = temp_char
                        writer_index += 1
                        temp_char = df['Old'][parser_index]
                    elif(df['Old'][parser_index] == "*"):
                        parser_index += 1
            elif(c_term_parsing):
                if(df['Old'][parser_index]=='C'):
                    if(df['Old'][parser_index+1]=='O'):
                        if(df['Old'][parser_index+2]=='O'):
                            if(df['Old'][parser_index+3]=='H'):
                                parser_index += 4
                                df['New'][writer_index] = 'O'
                                df['New'][writer_index+1] = 'H'
                                writer_index += 1
                c_term_parsing = False
            else:
                df['New'][writer_index] = df['Old'][parser_index].lower()
                parser_index += 1
                writer_index += 1

        new_seq = ""
        for i in range(pep_length):
            new_seq += df['New'][i]
        df_reduced['New_Sequence'][indexing] = new_seq

    df_reduced.to_csv('/mnt/compomics/Nicolas/Python/R2TF/data/project_transformed'+str(test['projectid'][projIndex])+'.csv',
                      index=False,header=False)

from pyteomics import parser
new_seq_2 = "H-QpyrQSEEDLLLQDFSR-OH"
parser.parse(new_seq_2, allow_unknown_modifications=True)
