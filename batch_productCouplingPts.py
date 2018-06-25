# Author: Emily (Millie) McDonald, The University of Melbourne

import sys
print(sys.version)
import os
import subprocess
import time
import math

import re
import numpy as np

def coreWidth(factor,mf,M):
    return (factor * (M**2 - 4. * mf**2) * np.sqrt(1. - (4. * mf**2)/M**2) )/(8. * math.pi * M)

def totalWidth(sinTheta,gx,mx,M):
    width = 0.
    vev = 246.
    for mq in [0.0023, 0.0048, 0.095, 1.28, 4.25, 174.]:
        if M > 2.*mq:
            width = width + coreWidth(3 * (sinTheta * mq/vev)**2, mq, M)
    if M > 2.*mx:
        width = width + coreWidth( (gx * mx / M)**2, mx, M)
    return width

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def unitarityReq(MY0, MXm, gAXm):
    eq = (gAXm*MXm)/(6*MY0)
    #eq = (gAXm*MXm)/(7*MY0)
    pair = []
    if eq < math.sqrt(math.pi):
        pair = ['true', eq]
    else:
        pair = ['false', eq]
    return pair 

homeDir = "/coepp/cephfs/mel/milliem/ThomasKarlPaper/monojet_13tev_workarea/darkmatter2mediatormodel/";
massCouplingPts = homeDir + "masspoints.dat"
failedPts = homeDir + "failedPts_product.dat"

if os.path.exists(failedPts):
    os.system("rm " + failedPts)
with open(failedPts, "a") as f:
    f.write("# Mmed (MY0)	mx	product    gAX\n")
successfulPts = homeDir + "successfulPts_product.dat"
if os.path.exists(successfulPts):
    os.system("rm " + successfulPts)
with open(successfulPts, "a") as f:
    f.write("# Mmed (MY0)       mx      product    gAX\n")

product = [0.01, 0.05, 0.075, 0.1, 0.25, 0.5, 0.7]
#product = [0.1, 0.5]
fgVq = 0.0
Theta = 0.3
nEvents = 10000
analysis_name = "ATLAS_2016_I1452559"

if os.path.exists(massCouplingPts):
    with open(massCouplingPts) as g:
        for line in g:
            if '#' not in line:
                array = re.split('\\s', line)
                sMmed = array[0]
                fMmed = float(sMmed) # scalar mass (MY0)
                smDM = array[1]
                fmDM = float(smDM)
#                sgAX = str(float(array[2]))
 #               fgAX = float(array[2])

                for element in product:

                    baseName = "Mmed" + sMmed + "_mDM" + smDM + "_PROD" + str(element).replace(".","p")
                    print "baseName = " + baseName

                    fgAX = (6.0*fMmed*pow(element,2))/(math.sin(Theta)*fmDM)
                    sgAX = str(fgAX)
                    print "gAX = " + sgAX
                
                    if fgAX >= math.sqrt(4.0*math.pi):
			with open(failedPts, "a") as f:
                            f.write(sMmed + "   " + smDM + "    " + str(element) + "    " + sgAX + " (gAX > sqrt(4pi))\n")
                        continue
                        
                    # First check gSXm is less than sqrt(pi)
                    check = unitarityReq(fMmed, fmDM, fgAX)
                    print "Point passes unitarity check = " +  check[0] + " with eq = " + str(check[1])

                    if check[0]=='false':
                        with open(failedPts, "a") as f:
                            f.write(sMmed + "	" + smDM + "	" + str(element) + "	" + sgAX + " (unitarity req)\n")
                        continue

                    tmpWidth = totalWidth(math.sin(Theta),fgAX,fmDM,fMmed)
                    print "Width = " + str(tmpWidth)

                    if tmpWidth>0.3*fMmed:
                        print "Width requirement failed"
                        with open(failedPts, "a") as f:
                            f.write(sMmed + "   " + smDM + "    " + str(element) + "    " + sgAX + " (width req)\n")
                        continue

                    with open(successfulPts, "a") as f:
                        f.write(sMmed + "   " + smDM + "    " + str(element) + "    " + sgAX + "\n")
                
                    script = "bash_submitRivet_" + baseName + ".sh"
                    bashScript = homeDir + script
    
                    os.system("cp submitMedDMRivet_scalar_product.sh " + bashScript)
                    os.system("sed -i 's/sY0Mmed/'" + str(fMmed) + "'/g' " + bashScript)
                    os.system("sed -i 's/sY1Mmed/'" + str(6.0*fMmed) + "'/g' " + bashScript)
                    os.system("sed -i 's/smDM/'" + str(fmDM) + "'/g' " + bashScript)
                    os.system("sed -i 's/sqVq/'" + str(fgVq) + "'/g' " + bashScript)
                    os.system("sed -i 's/sTheta/'" + str(Theta) + "'/g' " + bashScript)
                    os.system("sed -i 's/sgAx/'" + str(fgAX) + "'/g' " + bashScript)
                    os.system("sed -i 's/sAnalysis/'" + analysis_name + "'/g' " + bashScript)
                    os.system("sed -i 's/sOutFolder/'" + baseName + "'/g' " + bashScript)
                    os.system("sed -i 's/sEvents/'" + str(nEvents) + "'/g' " + bashScript)
                    os.system("sed -i 's/sQcut/'" + str(fMmed/4.0) + "'/g' " + bashScript)

                    scpDir = "." #directory where your run script is
	            logDir = "./logFiles/"  #directory for log files
		    jobName = "submitRivet_" + "Mmed" + sMmed + "_mDM" + smDM + "_PROD" + str(element).replace(".","p")

	    	    queue = "long"
		    #queue = "mel_long"
	    	    walt = "walltime=72:00:00"

                    os.system("qsub -q " + queue + " -l " + walt + " -l ncpus=4 -V -N " + jobName + " -e " + logDir + " -o " + logDir + " ./" + script)
                    os.system("mv " + bashScript + " " + homeDir + "bash_scripts/")
