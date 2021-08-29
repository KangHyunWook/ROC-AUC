"""
Precision recall curve for biased test_roc.py
"""

import numpy as np

def getNumbers(testy, preds):    #calculate num. of true positives and false negatives
    nfn=0
    ntp=0
    nfp=0
    ntn=0

    for i in range(len(preds)):
        print('preds:', preds)
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
        if prob[1] >= threshold:
            preds.append(1)
        else:
            preds.append(0)
    return preds

def getrates(testy, probs, skilled=1):
    recallList=[]
    precisionList=[]
    for i in range(len(threshold)):
        thresh=threshold[i]
        preds=getPreds(probs, thresh) #return prediction result given with the corresponding threshold. 
        nfn, ntn, ntp, nfp = getNumbers(testy, preds)
        
        # if skilled==0:
            # print('threshold:',thresh)
            # print('nfn, ntn, ntp, nfp:', nfn, ntn, ntp, nfp)
        recall=ntp/(ntp+nfn)
        if ntp==0 and nfp==0:
            precision='nan'
        else:
            precision=ntp/(ntp+nfp)
        
        recallList.append(recall)
        precisionList.append(precision)
    return recallList, precisionList


threshold=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
testy=[0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0] #event
#probability returned by skilled model
probs=[[0.9, 0.1],
       [0.8, 0.2],
       [0.7, 0.3],
       [0.1, 0.9],
       [0.6, 0.4],
       [0.9, 0.1],
       [0.8, 0.2],
       [0.2, 0.8],
       [0.7, 0.3],
       [0.6, 0.3],
       [0.8, 0.2],
       [0.3, 0.7],
       [0.9, 0.1],
       [0.8, 0.2],
       [0.9, 0.1]]
       
probs=np.array(probs)       
print(probs)

"""true positive rate=true positives/(true positives+false negatives)"""
print('thre:',threshold)
preds=[] #variable to store predictions

skilled_recallList, skilled_precisionList =getrates(testy, probs)

#probability returned by no skilled model
probs=[[0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
       [0.9, 0.1],
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

#no skilled recall and precision list are returned by getrates function
ns_recallList, ns_precisionList=getrates(testy, probs, 0)

from matplotlib import pyplot

skilled_recallList=skilled_recallList[:9]
skilled_precisionList=skilled_precisionList[:9]
ns_recallList=ns_recallList[:9]
ns_precisionList=ns_precisionList[:9]

print(skilled_recallList)
print(skilled_precisionList)
print(ns_recallList)
print(ns_precisionList)
ns_precisionList[1]=ns_precisionList[0] 
pyplot.plot(skilled_recallList, skilled_precisionList, linestyle='--', label='skilled')
pyplot.plot(ns_recallList[:2], ns_precisionList[:2], marker='.', label='no skilled')
pyplot.xlabel("recall")
pyplot.ylabel("precision")

pyplot.legend()
pyplot.show()




