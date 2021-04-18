from numpy import random
from statistics import median
def hash(X,a,b,t):
    return (((a*X+b)%48623)%t)

def generate_salt(n):
    salt=list()
    salt=[[random.randint(1,10000),random.randint(1,10000)] for i in range(n)]
    return salt    

class count_min():
    def __init__(self,w,d):
        self.w=w
        self.d=d
        self.salt=generate_salt(w)
        self.A=[[0]*d for i in range(w)]

    def Process(self,X,C):
        for i in range(self.w):
            self.A[i][hash(X,self.salt[i][0],self.salt[i][1],self.d)]+=C

    def Query(self,Q):
        min=10**8
        for i in range(self.w):
            temp=self.A[i][hash(Q,self.salt[i][0],self.salt[i][1],self.d)]
            if(temp<min):
                min=temp
        return min        

class count_sketch():
    def __init__(self,w,d):
        self.w=w
        self.d=d
        self.salt_h=generate_salt(w)
        self.salt_g=generate_salt(w)
        self.A=[[0]*d for i in range(w)]

    def Process(self,X,C):
        for i in range(self.w):
            if(hash(X,self.salt_g[i][0],self.salt_g[i][1],self.d)==1):
                self.A[i][hash(X,self.salt_h[i][0],self.salt_h[i][1],self.d)]+=C
            else:
                self.A[i][hash(X,self.salt_h[i][0],self.salt_h[i][1],self.d)]-=C

    def Query(self,Q):
        res=list()
        for i in range(self.w):
            if(hash(Q,self.salt_g[i][0],self.salt_g[i][1],self.d)==1):
                res.append(self.A[i][hash(Q,self.salt_h[i][0],self.salt_h[i][1],self.d)])
            else:
                res.append(-self.A[i][hash(Q,self.salt_h[i][0],self.salt_h[i][1],self.d)])
        return median(res)

class MG():
    def __init__(self,k):
        self.k=k
        self.counter={}
    def Process(self,X,C):
        
        if(X in self.counter):
            self.counter[X]+=C
        elif(len(self.counter)<self.k):
            self.counter[X]=C
        else:
            if(C<=min(self.counter.values())):
                for j in self.counter:
                    self.counter[j]-=C
            else:
                m=min(self.counter.values())
                for j in self.counter:
                    self.counter[j]-=m
                for i in self.counter:
                    if(self.counter[i]==0):
                        self.counter.pop(i)
                        self.counter[X]=C-m    
                        break
    def Query(self,Q):
        if(Q in self.counter):
            return self.counter[Q]
        else:
            return 0  