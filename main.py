import numpy as np
N=50
M=3

my_list =[-1,1]
a=[np.random.choice(my_list,N) for j in range(M)]
W=np.zeros((50,50))
for i in range (N):
    for j in range(N):
        if i==j : 
            W[i][j]=0
        else :
            for k in range (M):
                W[i][j]+=(1/M)*a[k][i]*a[k][j]
                


