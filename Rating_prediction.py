import numpy as np
from numpy import linalg as la
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(24)
#Getting rating data
a=pd.read_csv('ratings.csv')
req=np.array(a.iloc[:,:-1])
userID=np.unique(req[:,0])
MovieID=np.unique(req[:,1])
movie_map=dict()
#Store Movie Id using a key starting from 0
for i in range(len(MovieID)):
    movie_map[MovieID[i]]=i

#Mixing the given data and spliting into Test and Train data, with Train containing 80% data    
mix=a.sample(frac=1).reset_index(drop=True)
split_at=int(0.8*(a.shape[0]))
Train=np.array(mix.iloc[:split_at,:-1])
Test=np.array(mix.iloc[split_at:,:-1])

#This is original user movie rating matrix
R=np.zeros((userID.shape[0],MovieID.shape[0]))

#This is training matrix
S=np.empty((userID.shape[0],MovieID.shape[0]))
S[:,:]=np.nan

#Filling R
for i in range(len(req)):
    R[int(req[i,0]-1),int(movie_map[req[i,1]])]=req[i,2]

#Filling S
for i in range(len(Train)):
    S[int(Train[i,0]-1),int(movie_map[Train[i,1]])]=Train[i,2]
#Filling blank space of S with average UserRatings
for i in range(S.shape[0]):
    tp=S[i,:]
    tp[np.isnan(tp)]=np.nanmean(tp)
    S[i,:]=tp

#Finding K-rank approximation    
U,Sig,V=la.svd(S)    
err=list() #Contains list of errors
for k in range(1,100):
    #Just to know number of iterations completed
    if(k%10==0):
        print("Done {} Iterations".format(k))
    Trained_Matrix=U[:,:k]@np.diag(Sig[:k])@V[:k,:]
    Trained_Matrix=np.where(Trained_Matrix<0,0,Trained_Matrix)
    Trained_Matrix=np.where(Trained_Matrix>5,5,Trained_Matrix)
    # Find Error: 
    error=0
    for i in range(len(Test)):
        error+=(R[int(Test[i,0]-1),int(movie_map[Test[i,1]])]-Trained_Matrix[int(Test[i,0]-1),int(movie_map[Test[i,1]])])**2
    err.append(error)
x_axis=list(range(1,100))

#Plot graph 
plt.plot(x_axis,err)
plt.xlabel("K value")
plt.ylabel("Mean Square error")
plt.title("Graph for Rank-k approximation")
plt.savefig('q5.png')
plt.show()