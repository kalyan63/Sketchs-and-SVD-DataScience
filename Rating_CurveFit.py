import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# This function is used fit the curve
def  pred(X,a,b):
    return X[:,0]*a +X[:,1]*b

#Get data and make Movie map to store movie ids 
np.random.seed(24)
a=pd.read_csv('ratings.csv')
req=np.array(a.iloc[:,:-1])
userID=np.unique(req[:,0])
MovieID=np.unique(req[:,1])
movie_map=dict()
for i in range(len(MovieID)):
    movie_map[MovieID[i]]=i

#Mixing and spliting data into Train and Test
mix=a.sample(frac=1).reset_index(drop=True)
split_at=int(0.8*(a.shape[0]))
Train=np.array(mix.iloc[:split_at,:-1])
Test=np.array(mix.iloc[split_at:,:-1])

#This is training matrix
S=np.empty((userID.shape[0],MovieID.shape[0]))
S[:,:]=np.nan

#Filling S to easily find average ratings of users and movies
for i in range(len(Train)):
    S[int(Train[i,0]-1),int(movie_map[Train[i,1]])]=Train[i,2]

#Finding average user and movie rating from Train data using S matrix
User_avgrting=dict()
Movie_avgrting=dict()
#Get Average User rating
for i in range(S.shape[0]):
    tp=np.nanmean(S[i,:])
    if(np.isnan(tp)):
        User_avgrting[i]=3.5
    else:    
        User_avgrting[i]=tp
#Get Average Movie rating        
for i in range(S.shape[1]):
    tp=np.nanmean(S[:,i])
    if(np.isnan(tp)):
        Movie_avgrting[i]=3.5
    else:
        Movie_avgrting[i]=tp

# Here we store Average rating for user and movie according to the Train set
# Then we store Rating given by the user to a perticular movie in y
X=list()
y=list()
for i in range(len(Train)):
    X.append([User_avgrting[Train[i,0]-1],Movie_avgrting[movie_map[Train[i,1]]]])
    y.append(Train[i,2])
X=np.array(X)
y=np.array(y)

# Curve fitting
coef,_=curve_fit(pred,X,y)
print("The value of coefficients for curve fitting is: {}".format(coef))

#Testing with test data
X_test=list()
for i in range(len(Test)):
    X_test.append([User_avgrting[Test[i,0]-1],Movie_avgrting[movie_map[Test[i,1]]]])
X_test=np.array(X_test)    
y_hat=pred(X_test,coef[0],coef[1])
print("The error for Baseline model is: {}".format(np.sum((y_hat-X_test[:,-1])**2)))