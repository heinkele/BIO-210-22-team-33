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

a_0l = np.random.randint(3)
a_1l = np.random.randint(3)
a_2l = np.random.randint(3)
a_0c = np.random.randint(50)
a_1c = np.random.randint(50)
a_2c = np.random.randint(50)

while (a_0l == a_1l) and (a_0c == a_1c) :
    while (a_0l == a_2l) and (a_0c == a_2c) :
        while (a_1l == a_2l) and (a_1c == a_2c) :

            a_1l = np.random.randint(3)
            a_2l = np.random.randint(3)
            a_1c = np.random.randint(50)
            a_2c = np.random.randint(50)  ##generation de 3 indexations aléatoires différentes pour créer p_0

p_0 = a

p_0[a_0l][a_0c] *= -1
p_0[a_1l][a_1c] *= -1
p_0[a_2l][a_2c] *= -1       ##Changement de trois valeurs aléatoires dans W


T = 0    ##Nb max itération bouce while 
while (p_0 != a) and (T < 20) :   
    for i in range (3) : 
        for j in range (50) : 
            if p_0[i][j] * W[i][j] >= 0 :
                p_0[i][j] = 1
            else :
                p_0[i][j] = -1

    T += 1

print(W, "\n\n\n", p_0)

