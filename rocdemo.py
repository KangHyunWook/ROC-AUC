import numpy as np
import os

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

def getPreds(fw, probs, threshold, testy):
    preds=[]
    for i in range(len(probs)):
        result='TP'
        pred=1
        if probs[i][1] >= threshold:
            pred=1
        else:
            pred=0
        if pred==1:
            if pred==testy[i]:
                result='TP'
            else:
                result='FP'
        else:
            if pred==testy[i]:
                result='TN'
            else:
                result='FN'
            
        preds.append(pred)
        fw.write('{}, {}, {}, {}\n'.format(probs[i], pred, events[i], result))
    return preds

def getrates(probs, _output_dir):
    tprList=[]
    fprList=[]
    output_dir=_output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i in range(len(threshold)):
        thresh=threshold[i]
        file_name='th{}.csv'.format(thresh)
        fw= open(os.path.join(output_dir,file_name), 'w')
        fw.write("Probabilities, Prediction, Events, Result\n")
        print('thre:',thresh)
        
        preds=getPreds(fw, probs, thresh, events)
        print(preds)
        nfn, ntn, ntp, nfp = getNumbers(events, preds)
        
        print(ntp,ntn, nfn, nfp)
        tpr=ntp/(ntp+nfn)        
        fpr=nfp/(nfp+nfn)
        fw.write('FPR:{}, TPR:{}\n'.format(fpr, tpr))
        print('tpr:',tpr,'fpr:',fpr)
        fprList.append(fpr)
        tprList.append(tpr)
        
        fw.close()
    return fprList, tprList

threshold=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
events=[0, 0, 1, 1, 0, 0, 1 , 0, 1, 0] #event
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

preds=[] #variable to store predictions

skilled_fprList, skilled_tprList =getrates(probs, './sklled_balancec')
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

"""No skilled model example """
ns_fprList, ns_tprList=getrates(probs, './no_skilled_balanced')

from matplotlib import pyplot
# pyplot.scatter(skilled_fprList, skilled_tprList, label='skilled')
# pyplot.show()
pyplot.plot(skilled_fprList, skilled_tprList, linestyle='--', label='skilled')
pyplot.plot(ns_fprList, ns_tprList, marker='.', label='no skilled')
pyplot.xlabel("False positive rate")
pyplot.ylabel("True positive rate")

pyplot.legend()
pyplot.show()















