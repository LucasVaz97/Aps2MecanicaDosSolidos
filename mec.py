import numpy as np
import math as m


def readDic(filename):
    dic = {}
    f = open(filename, "r")
    auxiliar = ""
    for x in f:
        if(x[0] == "*"):
            auxiliar = x.rstrip()
            dic[auxiliar] = []
            counter = 0
        if(x[0] != '*'):
            dic[auxiliar].append(x.rstrip())

    for i in dic:
        for j in range(len(dic[i])):
            dic[i][j] = dic[i][j].split()
            for k in range(len(dic[i][j])):
                try:
                    dic[i][j][k] = float(dic[i][j][k])
                except ValueError:
                    p = 0


def calcMRigidez(e, a, l, pontoA, pontoB):

    alfa = m.atan2(pontoB[1]-pontoA[1], pontoB[0]-pontoA[0])
    c = m.cos(alfa)
    s = m.sin(alfa)

    M = np.array([[c**2, c*s, -c**2, -c*s],
                  [c*s, s**2, -c*s, -s**2],
                  [-c**2, -c*s, c**2, c*s],
                  [-c*s, -s**2, c*s, s**2]])

    M = M.round(7)
    return ((e*a/l)*M)


def Gauss(F, M, tolerancia, loopN):

    u = np.zeros((len(M[0]), 1))
    uv = np.zeros((len(M[0]), 1))

    checkt2 = 0
    loop = 0

    while(True and (loop < loopN)):

        index = 0
        checkt1 = 0
        for i in range(len(M)):
            soma = 0
            for j in range(len(M[i])):
                soma += M[i][j]*u[j][0]
            uv[i][0] = u[i][0]
            u[i][0] = (F[i][0] - soma + u[i][0] * M[i][index]) / M[i][index]
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
