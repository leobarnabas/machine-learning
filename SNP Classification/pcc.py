import sys
import os
import math
import traceback

## Program takes training data, label files as arguments
try:
    
    ### Read data
    DEBUG=False
    datafile = sys.argv[1]
    f = open(os.path.join(os.path.dirname(__file__),datafile))
    data = []
    i=0;

    l = f.readline()
    while(l != ''):
            a = l.split()
            l2 = []
            for j in range(0,len(a),1):
                    l2.append(int(a[j]))
            data.append(l2)
            l = f.readline()

    rows = len(data)
    cols = len(data[0])
    f.close()

    ### Read labels
    labelfile = sys.argv[2]
    f = open(os.path.join(os.path.dirname(__file__),labelfile))
    labels =[]
    l = f.readline()
    while(l != ''):
            a = l.split()
            l2=[]
            l2.append(int(a[0]))
            l2.append(int(a[1]))
            labels.append(l2)
            l = f.readline()

    ymean=0
    ysd=0

    for i in range(0,rows,1):
        ymean+=labels[i][0]
    ymean/=rows

    for i in range(0,rows,1):
        ysd+=(ymean-labels[i][0])**2
    ysd=math.sqrt(ysd)

    pearsoncc=[]
    for j in range(0,cols,1):
        numr=0
        xmean=0
        xsd=0
        for i in range(0,rows,1):
            xmean+=data[i][j]
        xmean/=rows
        for i in range(0,rows,1):
            xsd+=(xmean-data[i][j])**2
        xsd=math.sqrt(xsd)
        for i in range(0,rows,1):
            numr+=(xmean-data[i][j])*(ymean-labels[i][0])
        deno=ysd*xsd
        if deno==0:
            r=0
        else:
            r=numr/deno
        if r<0:
            r*=-1
        pearsoncc.append(r)

    output=open(os.path.join(os.path.dirname(datafile),"output.pcc"),"w")
    for i in range(0,cols,1):
        output.write(str(pearsoncc[i])+"\n")
    output.close()

except Exception as err:
    print("Error executing the program:",err)
    traceback.print_exc()

    
