import os
import sys

## The program reads file with values full of True label and Predicted label separated by tab

def getLabels(filename):
    trueLbl=[]
    prdctdLbl=[]
    file=open(filename)
    lstLbl=file.readlines()
    ##print("Contents of the file...")
    for el in lstLbl:
        ##print(el)
        lbls=el.split('\t')
        trueLbl.append(int(lbls[0]))
        prdctdLbl.append(int(lbls[1]))
    return trueLbl,prdctdLbl

trueLbl,prdctdLbl=getLabels(os.path.join(os.path.dirname(__file__),sys.argv[1]))

if len(trueLbl)==len(prdctdLbl):
    ##print("True Label:",trueLbl)
    ##print("Predicted Label:",prdctdLbl)
    tp,fp,fn,tn=0,0,0,0

    ## Calculate TP, FP, TN, FN from the labels
    for i in range(0,len(trueLbl),1):
        if trueLbl[i]==1 and prdctdLbl[i]==1:
            tp+=1
        elif trueLbl[i]==-1 and prdctdLbl[i]==1:
            fp+=1
        elif trueLbl[i]==1 and prdctdLbl[i]==-1:
            fn+=1
        elif trueLbl[i]==-1 and prdctdLbl[i]==-1:
                tn+=1
##    print("True Positive",tp)
##    print("False Positive",fp)
##    print("False Negative",fn)
##    print("True Negative",tn)

    ## Calculate E, BER, Precision and Recall
    e=(fp+fn)/(tp+fp+fn+tn)
    ##ber=0.5*((fp/(fp+tn))+(fn/(fn+tp)))
    ##precision=tp/(tp+fp)
    ##recall=tp/(tp+fn)

    print(e)
    ##print("BER:",ber)
    ##print("Precision:",precision)
    ##print("Recall:",recall)
else:
    print("Inavlid File format. Please ensure that the program reads file with values full of True label and Predicted label separated by tab")
