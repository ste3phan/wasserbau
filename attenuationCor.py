#-------------------------------------------------------------------------------
# Name:        attenuationCor.py
# Purpose:
#
# Author:      stephan lindauer
# Institute:   bergische university of wuppertal
#
# Created:     10.03.2014
# Copyright:   (c) lindauer 2014
# Licence:     MIT
#
# Description: attenuation correction of processed RADOLAN DX data based
#              on Kraemer algorithm
#
# Requirement: processed RADOLAN DX Data with wradlib.io.readDX
#-------------------------------------------------------------------------------

import csv
import os

# enter data directory here
datadir = 'DataT4/'
# enter where to write new data
exp = 'DataOut/'

# entry parameters for correcting the attenuation
alpha=1*10**(-5)
beta=0.90

files = os.listdir(datadir)
processfile=0

# processes all files in datadir
for processfile in files:

    ifile = open(datadir+processfile, "rb")
    reader = csv.reader(ifile, delimiter=' ')
    ofile = open(exp+processfile, "wb")
    writer = csv.writer(ofile, delimiter=';')
    
    daten=[]
    
    for lines in reader:
        lineNum = 1
        # lineNum should be maximum line numbers of input files with standard value of 360
        while lineNum <= 360:
            # dbzA = entry value for correction
            dbzA=0
            dataKor=[]
            dataDBZ=[]
            if reader.line_num == lineNum:
                eleNum = 0
                while eleNum < len(lines):
                    # no correcting for first value
                    if eleNum == 0:
                        dM = float(lines[eleNum])+dbzA
                    # correction for attenuation for all other elements
                    else:
                        if float(dataKor[eleNum-1]/10) > 60:
                            dbzA = 2.50
                        else:
                            dbzA=alpha*((10**((float(dataKor[eleNum-1]))/10))**beta)
                        dM = (float(lines[eleNum]))+dbzA+sum(dataDBZ)
                    dataDBZ.append(dbzA)
                    eleNum+=1
                    dataKor.append(dM)
                writer.writerow(dataKor)
            lineNum+=1
   
    ifile.close()
    ofile.close()
