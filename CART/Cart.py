import sys
import os
from operator import itemgetter, attrgetter

### Program takes datafile and label file as command line arguments and outputs the prediction in a new file

class Node():
    feature=0
    value=0
    label=0
    bestsplt=0
    left=None
    right=None
        
def getLabels(bestsplt,data):
    lminus=0
    lplus=0

    rminus=0
    rplus=0
    
    for k in range(0,bestsplt,1):
        if data[k][0]==-1:
            lminus+=1
        else:
            lplus+=1

    for m in range(bestsplt,len(data),1):
        if data[m][0]==-1:
            rminus+=1
        else:
            rplus+=1
    return lminus,lplus,rminus,rplus

def gini(lp,lsize,rp,rsize,rows):
    #print(lp,lsize,rp,rsize,rows)
    return (lsize/rows)*(lp/lsize)*(1 - lp/lsize) + (rsize/rows)*(rp/rsize)*(1 - rp/rsize)

def getbestsplit(data,j):
    ##print("data",data)
    splts=[]
    gindex=[]

    fval=data[0][j]
    ##splts.append(0)
    for i in range(1, len(data), 1):
        if data[i][j]!=fval:
            splts.append(i)
            fval=data[i][j]

    ##print(splts)
   
    for k in splts:
        lstart=0
        lend=k
        rstart=lend
        rend=len(data)
        lp=0
        rp=0

        for i in range(0, len(data), 1):
            if i<lend and data[i][0]==float(-1):
                lp+=1
            elif i>=rstart and i<rend and data[i][0]==float(-1):
                rp+=1
        if lend==0 or (rend-rstart)==0:
            gindex.append(0)
        else:
            gindex.append(gini(lp,lend,rp,rend-rstart,len(data)))
            
        

    if len(splts)>0:
        bestgini=min(gindex)
        bestsplit=splts[gindex.index(bestgini)]
    else:
        bestsplit=-1
        bestgini=-1
        
    
    
    return bestgini,bestsplit

    

    
     

def recurse(data,node):
    ##print(node)
    cols=len(data[0])
    bestsplits=[]
    bestgindices=[]
    for i in range(1, cols, 1):
        data.sort(key=itemgetter(i))
        bestgini,bestsplit=getbestsplit(data,i)
        if bestsplit>-1 and bestgini>-1:
            bestsplits.append(bestsplit)
            bestgindices.append(bestgini)

    if len(bestgindices)>0:
        bestgi=min(bestgindices)
        bestsplt=bestsplits[bestgindices.index(bestgi)]
        bestcolumn=bestgindices.index(bestgi)+1
        data.sort(key=itemgetter(bestcolumn))
        node.feature=bestcolumn
        node.value=data[bestsplt-1][bestcolumn]
        node.bestsplt=bestsplt

        if bestgi<0.05:
            return
    else:
        return
        
    
        ##print("best gini for feature with value:",node.feature,bestgi,node.value)
        
    
    
##    print("data",data)
##    print("best column:",bestcolumn)
##    print("best split value:",data[bestsplt-1][bestcolumn])
##    print("best gini value:",bestgi)

    lminus,lplus,rminus,rplus=getLabels(node.bestsplt,data)
    ##print(lminus,lplus,rminus,rplus)
    if lminus==0 or lplus==0:
        child=Node()
        if lplus==0:
            child.label=-1
        else:
            child.label=1
        node.left=child
    else:
        dataneg=data[0:bestsplt]
        lnode=Node()
        node.left=lnode
        recurse(dataneg,lnode)

        lminus,lplus,rminus,rplus=getLabels(lnode.bestsplt,dataneg)
        ##print(lminus,lplus,rminus,rplus)
        if lminus==0 or lplus==0:
            child=Node()
            if lplus==0:
                child.label=-1
            else:
                child.label=1
            lnode.left=child
        else:
            child=Node()
            if lminus>lplus:
                child.label=-1
            else:
                child.label=1
            lnode.left=child
            ##print("unclassified in left")
            
        if rplus==0 or rminus==0:
            child=Node()
            if rplus==0:
                child.label=-1
            else:
                child.label=1
            lnode.right=child
        else:
            child=Node()
            if rminus>rplus:
                child.label=-1
            else:
                child.label=1
            lnode.right=child
        
    if rplus==0 or rminus==0:
        child=Node()
        if rplus==0:
            child.label=-1
        else:
            child.label=1
        node.right=child
    else:
        datapos=data[bestsplt:]
        rnode=Node()
        node.right=rnode
        recurse(datapos,rnode)
        
        lminus,lplus,rminus,rplus=getLabels(rnode.bestsplt,datapos)
        ##print(lminus,lplus,rminus,rplus)
        
        if lminus==0 or lplus==0:
            child=Node()
            if lplus==0:
                child.label=-1
            else:
                child.label=1
            rnode.left=child
        else:
            ##print("unclassified in right")
            child=Node()
            if lminus>lplus:
                child.label=-1
            else:
                child.label=1
            rnode.left=child
            
        if rplus==0 or rminus==0:
            child=Node()
            if rplus==0:
                child.label=-1
            else:
                child.label=1
            rnode.right=child
        else:
            child=Node()
            if rminus>rplus:
                child.label=-1
            else:
                child.label=1
            rnode.right=child
            
    
    
    
        
        

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
                l2.append(float(a[j]))
        data.append(l2)
        l = f.readline()

rows = len(data)
cols = len(data[0])
f.close()


if(DEBUG):
        for i in range(0, len(data), 1):
                print(data[i])

### Read labels

labelfile = sys.argv[2]
f = open(os.path.join(os.path.dirname(__file__),labelfile))
trainlabels ={}
l = f.readline()
while(l != ''):
        a = l.split()
        trainlabels[int(a[1])]=int(1) if int(a[0])==1 else int(-1)
        ##trainlabels.append(float(1) if int(a[0])==1 else float(-1))
        ##trainlabels.append(float(a[0]))
        l = f.readline()
        
testdata=[]
traindata=[]
for i in range(0,len(data), 1):
    if trainlabels.get(i)!=None:
        data[i].insert(0,trainlabels[i])
        traindata.append(data[i])
    else:
        testdata.append(data[i])
        
    

node=Node()
recurse(traindata,node)

if node.left==None:
    left=Node()
    left.label=-1
    node.left=left
    
if node.right==None:
    right=Node()
    right.label=1
    node.right=right
    
targetFile=open(os.path.splitext(datafile)[0]+".prediction","w")

for i in range(0,len(data),1):
    if trainlabels.get(i)==None:
        tmp=node
       
        while(tmp!=None and tmp.label==0):
##            print("data:",data[i][tmp.feature-1])
##            print("feature:",tmp.feature)
##            print("value:",tmp.value)
            if data[i][tmp.feature-1]>tmp.value:
                tmp=tmp.right
            else:
                tmp=tmp.left
        targetFile.write(str(tmp.label)+" "+str(i)+"\n")
