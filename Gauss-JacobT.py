import numpy as np
import math as m

M = np.array([[1.59,-0.40,-0.54],
              [-0.40,1.70,0.40],
              [-0.54,0.40,0.54],])
M=M*10**8

F=np.array([[0.0],[150.0],[-100]])

u=np.array([[0.0],[0.0],[0.0]])
uv = np.array([[0.0],[0.0],[0.0]])

tolerancia = 0.05 #input user
loopN = 30 # input user

checkt2 = 0
loop = 0

while(True and (loop < loopN)):
    index = 0
    checkt1 = 0
    for i in range(len(M)):
        soma=0
        for j in range(len(M[i])):
            soma += M[i][j]*u[j][0]
        uv[i][0] = u[i][0]
        u[i][0] = ( F[i][0] - soma + u[i][0] * M[i][index] ) / M[i][index]
        index += 1
        if(loop > 0):
            check = (u[i][0] - uv[i][0]) / u[i][0]
            if(check > checkt1):
                checkt1 = check
    if(loop > 0):
        checkt2 = checkt1
        if(checkt2 < tolerancia):
            break

    loop += 1
