import sys
import os
import math
import traceback
import subprocess

### Program takes the following arguments in command line, 1)ranked file 2)training file 3)true labels

def computeError(features,trainingdata,truelabel):
    newfeatures=open(str(len(features))+".dim","w")
    for j in range(0,len(features),1):
        newfeatures.write(str(features[j])+"\n")
    newfeatures.close()
    e=float(subprocess.check_output([sys.executable,"CrossValidation.py",trainingdata,truelabel,""+str(len(features))+".dim"]))
    return e


### Read features
## File with ranked features
rankfile=sys.argv[1]

trainingdata=sys.argv[2]
truelabel=sys.argv[3]

features=[]
rk=open(os.path.join(os.path.dirname(__file__),rankfile))

ln=rk.readline()
while(ln!=''):
    a=ln.split()
    features.append(int(a[0]))
    ln=rk.readline()


totalfeatures=len(features)
##features.sort()
i=0
accuracy=65
removed=int(0)
while i<totalfeatures:
    i+=1
    print(accuracy,len(features))
    if accuracy>63:
        removed=features.pop(0)
        e=computeError(features,trainingdata,truelabel)
        accuracy=(1-e)*100
    else:
        features.insert(len(features)-1,removed)
        removed=features.pop(0)
        e=computeError(features,trainingdata,truelabel)
        accuracy=(1-e)*100
        
    
