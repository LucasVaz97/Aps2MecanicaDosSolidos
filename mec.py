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

    return dic


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


def calcGauss(F, M, tolerancia, loopN):

    u = [0]*len(M[0])
    uv = [0]*len(M[0])

    checkt2 = 0
    loop = 0

    while(True and (loop < loopN)):

        index = 0
        checkt1 = 0
        
        for i in range(len(M)):
            soma = 0

            for j in range(len(M[i])):
                soma += M[i][j]*u[j]

            uv[i] = u[i]
            u[i] = (F[i][0] - soma + u[i] * M[i][index]) / M[i][index]
            index += 1

            if(loop > 0):
                check = (u[i] - uv[i]) / u[i]

                if(check > checkt1):
                    checkt1 = check
                    
        if(loop > 0):
            checkt2 = checkt1

            if(checkt2 < tolerancia):
                break

        loop += 1

    return u

def dicCalcMRigid(dic):

    listM = []
    coordinates = dic["*COORDINATES"]
    materials = dic["*MATERIALS"]
    geometric = dic["*GEOMETRIC_PROPERTIES"]
    
    for i in range(len(dic["*INCIDENCES"])):

        indexA = int(dic["*INCIDENCES"][i][1]) 
        indexB = int(dic["*INCIDENCES"][i][2])

        pontoA = [coordinates[indexA][1], coordinates[indexA][2]]
        pontoB = [coordinates[indexB][1], coordinates[indexB][2]]

        e = materials[i+1][0]
        a = geometric[i+1][0]
        l = m.hypot(pontoB[0] - pontoA[0], pontoB[1] - pontoA[1])
        
        listM.append(calcMRigidez(e, a, l, pontoA, pontoB))

    return listM

def finalU(u): #preenche a matriz u corretamente no formato u = [1, 2, 3, 4]
    pass


def makeExitFile(filename, u, strains, stresses):

    file = open(filename,"w")

    file.write("*DISPLACEMENTS\n")
    j = 1

    for i in range(0, len(u)-1, 2):
        file.write(str(j) + " ")
        file.write(str(u[i]) + " ")
        file.write(str(u[i+1]) + "\n")
        j += 1

    file.write("\n")
    file.write("*ELEMENT_STRAINS\n")
    j = 1
    for i in range(len(strains)):
        file.write(str(j) + " ")
        file.write(str(strains[i]) + "\n")
        j += 1

    file.write("\n")
    file.write("*ELEMENT_STRESSES\n")
    j = 1
    for i in range(len(stresses)):
        file.write(str(j) + " ")
        file.write(str(stresses[i]) + "\n")
        j += 1

    file.write("\n")
    file.write("*REACTION_FORCES\n")

M = np.array([[1.59e8,-0.40e8,-0.54e8],
              [-0.40e8,1.70e8,0.40e8],
              [-0.54e8,0.40e8,0.54e8],])

F=np.array([[0.0],[150.0],[-100]])

u = calcGauss(F, M, 0.005, 10)+[10]

ut = [1, 2, 3, 4]
strains = [1, 2, 3]
stresses = [1, 2, 3]

makeExitFile("saida.txt", ut, strains, stresses)
