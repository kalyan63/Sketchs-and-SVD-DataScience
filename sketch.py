from typing import Counter
import matplotlib.pyplot as plt
from numpy import random
from Sketch_main import count_min,count_sketch,MG
random.seed(42)
file=open('matlab/train.data','r')
wordIDX=list()
count=list()
for i in file:
    j=i.split()
    wordIDX.append(int(j[1]))
    count.append(int(j[2]))
freq=dict()
for i in range(len(wordIDX)):
    if(wordIDX[i] in freq):
        freq[wordIDX[i]]+=count[i]
    else:
        freq[wordIDX[i]]=count[i]
cnt=Counter(freq)
top1000=dict(cnt.most_common(1000))
a=list(top1000.keys())
random.shuffle(a)
test=a[:100]
k=[100,200,500,1000,2000]
errs=dict()
for i in k:
    print("start: {}".format(i))
    w=5
    d=i//w
    CM=count_min(w,d)
    CS=count_sketch(w,d)
    S=MG(i)
    for j in range(len(wordIDX)):
        CM.Process(wordIDX[j],count[j])
        CS.Process(wordIDX[j],count[j])
        S.Process(wordIDX[j],count[j])
    er_cm=er_cs=er_s=0
    print("Done Train: {}".format(i))
    for ts in test:
        er_cm+=0.01*(abs(top1000[ts]-CM.Query(ts))/top1000[ts])
        er_cs+=0.01*(abs(top1000[ts]-CS.Query(ts))/top1000[ts])
        er_s+=0.01*(abs(top1000[ts]-S.Query(ts))/top1000[ts])
    errs[i]=list([er_cm,er_cs,er_s])  
y_cm=list()
y_cs=list()
y_s=list()
for i in errs:
    y_cm.append(errs[i][0])
    y_cs.append(errs[i][1])
    y_s.append(errs[i][2])
plt.plot(k,y_cm,label='Count Min')
plt.plot(k,y_cs,label='Count Sketch')
plt.plot(k,y_s,label='Misra-Gries')  
plt.xlabel('K Values')
plt.ylabel('Error in Frequency')
plt.legend()  
plt.show()