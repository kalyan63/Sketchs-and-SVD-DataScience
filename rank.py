import numpy as np
from numpy import linalg as la
import pandas as pd
a=pd.read_csv('ratings.csv')
req=np.array(a.iloc[:,:-1])
userID=np.unique(req[:,0])
MovieID=np.unique(req[:,1])
movie_map=dict()
for i in range(len(MovieID)):
    movie_map[MovieID[i]]=i

#This is original user movie rating matrix
R=np.zeros((userID.shape[0],MovieID.shape[0]))

#This is training matrix
S=np.zeros((userID.shape[0],MovieID.shape[0]))

#Filling R
for i in range(len(req)):
    R[int(req[i,0]-1),int(movie_map[req[i,1]])]=req[i,2]

mix=a.sample(frac=1).reset_index(drop=True)
split_at=int(0.8*(a.shape[0]))
Train=np.array(mix.iloc[:split_at,:-1])
Test=np.array(mix.iloc[split_at:,:-1])

#Filling S
for i in range(len(Train)):
    S[int(Train[i,0]-1),int(movie_map[Train[i,1]])]=Train[i,2]

#Finding K-rank approximation    
U,Sig,V=la.svd(S)    
err=list()
for k in range(40,42):
    Trained_Matrix=Sig[0]*U[0].reshape(-1,1)@V[0].reshape(-1,1).T
    for i in range(1,k):
        Trained_Matrix+=Sig[i]*U[i].reshape(-1,1)@V[i].reshape(-1,1).T
    Trained_Matrix=np.where(Trained_Matrix<0,0,Trained_Matrix)
    Trained_Matrix=np.where(Trained_Matrix>5,5,Trained_Matrix)
    # Find Error: 
    error=0
    for i in range(len(Test)):
        error+=(R[int(Test[i,0]-1),int(movie_map[Test[i,1]])]-Trained_Matrix[int(Test[i,0]-1),int(movie_map[Test[i,1]])])**2
    err.append(error)

print(err)  