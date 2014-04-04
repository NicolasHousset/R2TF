__author__ = 'compomics'

import MySQLdb
import pandas.io.sql as psql
from pandas import DataFrame
import pandas as pd

def connect_to_mslims(_host, _user, _passwd, _db):
    """A function to connect to the MSLIMS database, returns the cursor"""
    mysql_cn = MySQLdb.connect(host=_host,
                         user=_user,
                         passwd=_passwd,
                         db=_db)
    return mysql_cn

con = connect_to_mslims("muppet03.ugent.be",
                      "nicolas",
                      "nicolas,13*",
                      "projects")

def importProjNumbersFromMSLIMS(_con, _projNumber):
    """A function to extract one project"""
    _test = psql.frame_query("""SELECT projectid FROM project WHERE projectid >= """+
    str(_projNumber), con = _con)
    return _test

def importDataFromProject(_con, _projNumber):
    """A function to extract the data from one project"""
    _test2 = psql.frame_query("""SELECT modified_sequence, rtsec, spectrum.l_projectid,
    l_lcrunid, lcrun.name, spectrumid, l_instrumentid,
    l_protocolid, lcrun.filecount, lcrun.creationdate, scanid,
    number, l_userid,identified, score, identitythreshold,
    confidence, DB, total_spectrum_intensity, mass_to_charge,
    spectrum.charge, accession, start, end
    FROM
    (spectrum LEFT JOIN scan ON spectrum.spectrumid = scan.l_spectrumid
    LEFT JOIN identification ON spectrum.spectrumid = identification.l_spectrumid
    RIGHT JOIN project ON spectrum.l_projectid = project.projectid
    RIGHT JOIN lcrun ON spectrum.l_lcrunid = lcrun.lcrunid)
    WHERE spectrum.l_projectid = """+str(_projNumber), con=_con)
    return _test2

# We limit ourselves for now to the most relevant information
nbVar = 8

# Here we define the projects we want to import
nbProjects = 1000
startingProject = 2000

test = importProjNumbersFromMSLIMS(con, startingProject)
VarNames = ['sequence','rtsec','projectid','lcrunid','lcrun.name','spectrumid','instrumentid','protocolid','filecount',
            'creationdate','scanid','number','userid','identified','score','identitythreshold','confidence','DB',
            'total_spectrum_intensity','mass_to_charge','charge','accession','start','end']

for projIndex in range(nbProjects):
    df = importDataFromProject(con, test['projectid'][projIndex])
    nbSpectrum = len(df)
    print projIndex
    print nbSpectrum
    df.to_csv('/mnt/compomics/Nicolas/Python/R2TF/data/project'+str(test['projectid'][projIndex])+'.csv',index=False,
              header=False)