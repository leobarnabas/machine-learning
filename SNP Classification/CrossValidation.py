import sys
import os
import math
import traceback
import subprocess

### Program takes arguments traindata trainlabel features testdata

try:
    ### Read Features based on rank
    rankfile=sys.argv[3]
    findex=[]
    rk=open(os.path.join(os.path.dirname(__file__),rankfile))

    ln=rk.readline()
    while(ln!=''):
        a=ln.split()
        findex.append(int(a[0]))
        ln=rk.readline()
    
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
            for j in range(0,len(findex),1):
                l2.append(float(a[findex[j]]))
##            
##            for j in range(0,len(a),1):
##                    l2.append(float(a[j]))
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
    trainstart=0
    splitlen=int(len(labels)/10)
    trainend=splitlen

    traindata=data[trainstart:trainend]
    ##trainlabel=labels[trainstart:trainend]

    traindataFile=open(os.path.join(os.path.dirname(datafile),"traindata_cv"),"w")
    for i in range(0,len(data),1):
        traindataFile.write(" ".join(repr(e) for e in data[i])+"\n")
    traindataFile.close()
    error=0
    e=float(0)
    for i in range(0,10,1):
        trainlabel=[]
        for j in range(0,len(labels),1):
            if not(j>=trainstart and j<trainend):
                trainlabel.append(labels[j])
        trainlabelFile=open(os.path.join(os.path.dirname(labelfile),"trainlabel_cv"),"w")
        for j in range(0,len(trainlabel),1):
                       trainlabelFile.write(" ".join(repr(e) for e in trainlabel[j])+"\n")
        trainlabelFile.close()

        ##c=sys.argv[4]
        os.system("NaiveBayes.py trainlabel_cv traindata_cv")
        os.system("Input_generator.py trueclass.txt traindata_cv.prediction")
        e=float(subprocess.check_output([sys.executable,"Algorithm_Evaluation.py","traindata_cv.classifier"]))
        #print(e)
        error+=e
        ##os.system("LR_Perceptron.py traindata_cv trainlabel_cv")
        ##os.system("svm_light.py traindata_cv trainlabel_cv trueclass.txt "+c)
        ##os.system("Input_generator.py trueclass.txt svm.prediction")
        ##os.system("Algorithm_Evaluation.py svm.classifier")

    
        
        trainstart=trainend
        trainend+=splitlen
    error/=10
    ##print("Error:",error)
    ##print("Accuracy:",(1-error)*100)
    print(error)
    if len(sys.argv)==5:
        
        ### Read Test data
        testdatafile=sys.argv[4]
        f = open(os.path.join(os.path.dirname(__file__),testdatafile))
        testdata = []

        l = f.readline()
        while(l != ''):
                a = l.split()
                l2 = []
                for j in range(0,len(findex),1):
                    l2.append(float(a[findex[j]]))

                testdata.append(l2)
                l = f.readline()

        ### Write modified test data
        testmod=open("testdata.mod","w")
        for i in range(0,len(testdata),1):
            testmod.write(" ".join(repr(e) for e in testdata[i])+"\n")
        testmod.close()
        os.system("NaiveBayes.py trueclass.txt traindata_cv testdata.mod")
    
except Exception as err:
    print("Error executing the program:",err)
    traceback.print_exc()
