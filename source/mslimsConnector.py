# -*- coding: utf-8 -*-
"""
Spyder Editor

Getting the data from MS-LIMS and storing it in .csv format

"""
import MySQLdb

def connect_to_mslims(_host, _user, _passwd, _db):
    """A function to connect to the MSLIMS database, returns the cursor"""
    db = MySQLdb.connect(host=_host,
                         user=_user,
                         passwd=_passwd,
                         db=_db)
    _cur = db.cursor()
    return _cur

cur = connect_to_mslims("muppet03.ugent.be",
                      "nicolas",
                      "nicolas,13*",
                      "projects")

def importProjNumbersFromMSLIMS(_cur, _projNumber):
    """A function to extract one project"""
    _cur.execute("""SELECT projectid FROM project WHERE projectid >= """+
    str(_projNumber))
    _test = _cur.fetchall()
    return _test

def importDataFromProject(_cur, _projNumber):
    """A function to extract the data from one project"""
    _cur.execute("""SELECT modified_sequence, rtsec, spectrum.l_projectid, 
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
                 WHERE spectrum.l_projectid = """+str(_projNumber))
    _test2 = _cur.fetchall()
    return _test2

# We limit ourselves for now to the most relevant information
nbVar = 8
separator = ", "
newLine = """\n"""

# Here we define the projects we want to import
nbProjects = 10
startingProject = 2000
test = importProjNumbersFromMSLIMS(cur, startingProject)

for projIndex in range(nbProjects):   
    test2 = importDataFromProject(cur, test[projIndex][0])
    nbSpectrum = len(test2)/nbVar
    print projIndex
    print nbSpectrum
    with open('/mnt/compomics/Nicolas/Python/R2TF/data/project'
    +str(test[projIndex][0])+'.csv', 'w') as f:
        for i in range(nbSpectrum):
            for j in range(nbVar):
                f.write(str(test2[i][j]))
                f.write(separator)
            f.write(newLine)

# Will write a csv file with data from the database


cur.close()            

    
    

   





