import numpy as np

def getNumbers(testy, preds):    #calculate num. of true positives and false negatives
    nfn=0
    ntp=0
    nfp=0
    ntn=0

    for i in range(len(preds)):
        if preds[i]==0:
            if testy[i]==1: #false negative case
                nfn+=1
            else:
                ntn+=1 #increase true negative case
        elif preds[i]==1:
            if testy[i]==1:
                ntp+=1
            else:
                nfp+=1
    return nfn, ntn, ntp, nfp

def getPreds(probs, threshold):
    preds=[]
    for prob in probs:
        if prob[0] >= threshold:
            preds.append(1)
        else:
            preds.append(0)
    return preds

def getrates(probs):
    tprList=[]
    fprList=[]
    for i in range(len(threshold)):
        thresh=threshold[i]
        print('thre:',thresh)

        preds=getPreds(probs, thresh)
        nfn, ntn, ntp, nfp = getNumbers(testy, preds)

        tpr=ntp/(ntp+nfn)        
        fpr=nfp/(nfp+nfn)
        
        tprList.append(tpr)
        fprList.append(fpr)
    return fprList, tprList

threshold=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
testy=[1, 1, 0, 0, 1, 1, 0 , 1, 0, 1]
probs=[[0.9, 0.1],
       [0.8, 0.2],
       [0.3, 0.7],
       [0.7, 0.3],
       [0.6, 0.4],
       [0.9, 0.1],
       [0.2, 0.8],
       [0.8, 0.2],
       [0.3, 0.7],
       [0.6, 0.4]]
       
probs=np.array(probs)       
print(probs)

"""true positive rate=true positives/(true positives+false negatives)"""
print('thre:',threshold)
preds=[] #variable to store predictions

skilled_fprList, skilled_tprList =getrates(probs)
probs=[[0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1]]
       
probs=np.array(probs)

ns_fprList, ns_tprList=getrates(probs)

from matplotlib import pyplot

pyplot.plot(skilled_fprList, skilled_tprList, linestyle='--', label='skilled')
pyplot.plot(ns_fprList, ns_tprList, marker='.', label='no skilled')
pyplot.xlabel("False positive rate")
pyplot.ylabel("True positive rate")

pyplot.legend()
pyplot.show()















