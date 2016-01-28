import sys
import os
import math

## The program takes arguments in sequence (label datafile)

### Read data
DEBUG=False
datafile = sys.argv[2]
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


f.close()

if(DEBUG):
        for i in range(0, len(data), 1):
                print(data[i])

##if len(sys.argv)==4:
##        testfile=sys.argv[3]
##        f=open(testfile)
##        testdata=[]
##        lst=[]
##        l=f.readline()
##        while(l!=''):
##                a=l.split()
##                for i in range(0,len(a),1):
##                        lst.append(float(a[i]))
##                data.append(lst)
##                l=f.readline()
##        print("data length:",len(data))
        
rows = len(data)
cols = len(data[0])
##Standardize the column data
##mod=[];
##for i in range(0,cols,1):
##    mod.append(0)
##
##for i in range(0,cols,1):
##    for j in range(0,rows,1):
##        mod[i]+=data[j][i]**2
##    mod[i]=math.sqrt(mod[i])
##
##for i in range(0,cols,1):
##    for j in range(0,rows,1):
##        data[j][i]=data[j][i]/mod[i]

### Read labels

labelfile = sys.argv[1]
f = open(os.path.join(os.path.dirname(__file__),labelfile))
trainlabels ={}
n = {}
l = f.readline()
while(l != ''):
        a = l.split()
        trainlabels[int(a[1])]=int(a[0])
        if(int(a[0]) in n):
                n[int(a[0])] += 1
        else:
                n[int(a[0])]=1
        l = f.readline()
        

if(DEBUG):
        for i in n:
                print(i)
        print(trainlabels)

        
### Calculate means

total=[]
## Pseudo count to avoid zero variance
for i in range(0,len(n),1):
        lst=[]
        for j in range(0,cols,1):
                lst.append(1)
        total.append(lst)

for i in range(0,rows,1):
        if(trainlabels.get(i) != None and trainlabels.get(i) in n):
                for j in range(0,cols,1):
                        total[list(n.keys()).index(trainlabels.get(i))][j] += data[i][j]

mean=[]   

for i in range(0,len(total),1):
        tmp=[]
        for j in range(0,cols,1):
                tmp.append(total[i][j]/ list(n.values())[i])
        mean.append(tmp)
##print("\nMean values,\n",mean)

        
### Calculate variance

d=[]
for i in range(0,len(mean),1):
        lst=[]
        for j in range(0,cols,1):
                lst.append(0)
        d.append(lst)
for i in range(0,rows,1):
        if(trainlabels.get(i) != None):
                for j in range(0,cols,1):
                        d[list(n.keys()).index(trainlabels.get(i))][j]+=(mean[list(n.keys()).index(trainlabels.get(i))][j]-data[i][j])**2

sd=[]
for i in range(0,len(d),1):
        tmp=[]
        for j in range(0,cols,1):
                tmp.append(math.sqrt(d[i][j]/ list(n.values())[i]))
        sd.append(tmp)
##print("\nStandard Deviation values,\n",sd)


### Output predictions
targetFile=open(os.path.splitext(datafile)[0]+".prediction","w")

for i in range(0,rows,1):
        if(trainlabels.get(i)==None):
                d=[0]*len(mean)
                for j in range(0,cols,1):
                      for k in range(0,len(mean),1):
                              d[k]+=((mean[k][j]-data[i][j])/sd[k][j])**2
                targetFile.write(str(list(n)[(d.index(min(d)))])+" "+str(i)+"\n")


targetFile.close()

if len(sys.argv)==4:
        testfile=sys.argv[3]
        testprdctn=open(os.path.splitext(testfile)[0]+".prediction","w")
        f=open(testfile)
        testdata=[]
      
        l=f.readline()
        while(l!=''):
                a=l.split()
                lst=[]
                for i in range(0,len(a),1):
                        lst.append(float(a[i]))
                testdata.append(lst)
                l=f.readline()
        d=[]
        cols=len(testdata[0])
        for i in range(0,len(testdata),1):
                d=[0]*len(mean)
                for j in range(0,cols,1):
                        for k in range(0,len(mean),1):
                                d[k]+=((mean[k][j]-testdata[i][j])/sd[k][j])**2
                testprdctn.write(str(list(n)[(d.index(min(d)))])+" "+str(i)+"\n")
        testprdctn.close()
        


