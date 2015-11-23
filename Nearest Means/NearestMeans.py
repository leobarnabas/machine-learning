import sys
import os

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

rows = len(data)
cols = len(data[0])
f.close()

if(DEBUG):
        for i in range(0, len(data), 1):
                print(data[i])

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


for i in range(0,len(n),1):
        lst=[]
        for j in range(0,cols,1):
                lst.append(0)
        total.append(lst)


for i in range(0,rows,1):
        if(trainlabels.get(i) != None and trainlabels.get(i) in n):
                for j in range(0,cols,1):
                        total[list(n.keys()).index(trainlabels.get(i))][j] += data[i][j]

mean=[]   
print("Mean values below,")
for i in range(0,len(total),1):
        tmp=[]
        for j in range(0,cols,1):
                tmp.append(total[i][j]/ list(n.values())[i])
        mean.append(tmp)
        print(tmp)

### Calculate distance of mean to each test point and write the predictions to file
targetFile=open(os.path.splitext(datafile)[0]+".prediction","w")
        
for i in range(0,rows,1):
        if(trainlabels.get(i) == None):
                d=[0]*len(mean)
                for j in range(0,cols,1):
                        for k in range(0,len(mean),1):
                                d[k]+=(mean[k][j]-data[i][j])**2
                #print(list(n)[(d.index(min(d)))]," ",i)
                
                targetFile.write(str(list(n)[(d.index(min(d)))])+" "+str(i)+"\n")





targetFile.close()
