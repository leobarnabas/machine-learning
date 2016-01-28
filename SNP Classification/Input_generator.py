import sys
import os

### Program takes arguments truelabel, predicted label
prdctd = sys.argv[2]
f = open(os.path.join(os.path.dirname(__file__),prdctd))
data = []
i=0;
prdctdlabels ={}
l = f.readline()
while(l != ''):
        a = l.split()
        prdctdlabels[int(a[1])]=int(a[0])
        l = f.readline()
f.close()


truLbl=sys.argv[1]
f = open(os.path.join(os.path.dirname(__file__),truLbl))
data = []
i=0;
truelabels ={}
l = f.readline()
while(l != ''):
        a = l.split()
        truelabels[int(a[1])]=int(a[0])
        l = f.readline()
f.close()

targetFile=open(os.path.splitext(prdctd)[0]+".classifier","w")

for i in prdctdlabels:
    if truelabels.get(i)==0 and prdctdlabels.get(i)==0:
        targetFile.write("-1"+"\t"+"-1\n")
    elif truelabels.get(i)==1 and prdctdlabels.get(i)==0:
        targetFile.write("1"+"\t"+"-1\n")
    elif truelabels.get(i)==1 and prdctdlabels.get(i)==1:
        targetFile.write("1"+"\t"+"1\n")
    elif truelabels.get(i)==0 and prdctdlabels.get(i)==1:
        targetFile.write("-1"+"\t"+"1\n")
targetFile.close()
