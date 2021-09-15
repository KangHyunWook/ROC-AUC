import numpy as np
import os
import argparse

def getNumbers(testy, preds):    #calculate num. of true positives and false negatives
    ntp=0
    nfn=0
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
                

    if nfn >ntn:
        temp=nfn
        nfn=ntn
        ntn=temp
        
    if nfp > ntp:
        temp=nfp
        nfp=ntp
        ntp=temp

    return ntp, ntn, nfp, nfn

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
        
        preds=getPreds(fw, probs, thresh, events)
        ntp, ntn, nfp, nfn = getNumbers(events, preds)
        fw.write('\ntp:{} tn: {} fp: {} fn: {}\n'.format(ntp, ntn, nfp, nfn)) 
        tpr=ntp/(ntp+nfn)        
        fpr=nfp/(nfp+ntn)
        
        fw.write('FPR:{}, TPR:{}\n'.format(fpr, tpr))
     
        fprList.append(fpr)
        tprList.append(tpr)
        
        fw.close()
    return fprList, tprList

thres=0.0
threshold=[]
gap=0.01
while 1:
    
    threshold.append(thres)
    if thres>0.999999999999: break
    thres+=gap
    thres=round(thres,2)

events=[] #event

ap=argparse.ArgumentParser()
ap.add_argument('--events', help='events true of false', required=True)

args=ap.parse_args()
args=vars(args)
"""read events"""

with open(args['events'], 'r', encoding='utf-8') as f:
    for line in f:
        data=line
        splits=data.split(',')
        for split in splits:
            split.strip()
            events.append(int(split))
print(events)

"""Create skilled model"""

probs=[]
import random
random.seed(2)

mid=0.5
skilled_prob=0.1

def swap(a, b):
    temp=a
    a=b
    b=temp
    return a, b
    
for i in range(len(events)):
    ran=random.random()
    higher_prob=round(ran,2)
    lower_prob=round(1-ran,2)
    if higher_prob<lower_prob:
        higher_prob,lower_prob=swap(higher_prob,lower_prob)
    print(higher_prob, lower_prob)
    """if probabilty is greater than 0.1 prediction is right"""
    ran_prob=random.random()
    if ran_prob>=skilled_prob: #True prediction
        if events[i]==1:
            probs.append([lower_prob, higher_prob])
        else:
            probs.append([higher_prob, lower_prob])
    else: #False prediction
        if events[i]==1:
            probs.append([higher_prob, lower_prob])
        else:
            probs.append([lower_prob, higher_prob])
            
        
probs=np.array(probs)       

"""true positive rate=true positives/(true positives+false negatives)"""

preds=[] #variable to store predictions

skilled_fprlist, skilled_tprlist =getrates(probs, './sklled_balanced')
coordSet=set()
for i in range(len(skilled_fprlist)):
    print('===a===')

    a=skilled_fprlist[i]
    print(a)
    b=skilled_tprlist[i]
    coordSet.add((a,b))

coordList=sorted(list(coordSet))
print('===coordset===')
print(coordSet)
# print(coordList)

skilled_fprlist=[]
skilled_tprlist=[]
print('===coords===')
for coord in coordList:
    fpr, tpr=coord    
    skilled_fprlist.append(fpr)
    skilled_tprlist.append(tpr)

    print(fpr, tpr)    

probs=[]
for _ in range(len(events)):
    probs.append([0.9, 0.1])
       
probs=np.array(probs)

"""no skilled model example """
ns_fprlist, ns_tprlist=getrates(probs, './no_skilled_balanced')

from matplotlib import pyplot
pyplot.scatter(skilled_fprlist, skilled_tprlist, label='skilled')
pyplot.show()
pyplot.plot(skilled_fprlist, skilled_tprlist, linestyle='--', label='skilled')
pyplot.plot(ns_fprlist, ns_tprlist, marker='.', label='no skilled')
pyplot.xlabel("false positive rate")
pyplot.ylabel("true positive rate")

pyplot.legend()
pyplot.show()




