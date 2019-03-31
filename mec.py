import numpy as np
import math as m

def calcProdutoEscalar(p1, p2, vetor):
	u1 = vetor[0]
	v1 = vetor[1]
	u2 = vetor[2]
	v2 = vetor[3]
	x = abs(p1[0] - p2[0])
	y = abs(p1[1] - p2[1])
	h = (x**2 + y**2)**(1/2)
	CS = [0,0,0,0]
	CS[0] = -(x/h)
	CS[1] = -(y/h)
	CS[2] = (x/h)
	CS[3] = (y/h)
	resultado = 0
	for i in range(4):
		resultado += vetor[i]*CS[i]
	return resultado

def retornaglobalpronta(matrizes,grausLib,restricao):

	NoX = []
	NoY = []

	for i in range(len(grausLib)):
		for j in range(len(restricao)):
			if restricao[j][0] in grausLib[i]:
				if restricao[j][1] == 1:
					if restricao[j][0] not in NoX:
						NoX.append(restricao[j][0])
				else:
					if restricao[j][0] not in NoY:
						NoY.append(restricao[j][0])

	tamanho = len(set(list(np.concatenate(grausLib))))

	Global = np.zeros((tamanho, tamanho), dtype='float')

	for i in range(len(matrizes)):
		for x in range(len(matrizes[i])):
			for y in range(len(matrizes[i])):
				Global[grausLib[i][y] - 1, grausLib[i][x] - 1] += matrizes[i][y,x]

	NoX = np.array(NoX)
	NoX -= 1
	NoY = np.array(NoY)
	NoY -= 1

	lista = []
	lista_temporaria = []
	NoX += 1
	NoY += 1

	No = list(set(np.concatenate([NoX,NoY])))
    old_global = Global
	Global = np.delete(Global, No, 0)
	Global = np.delete(Global, No, 1)

	for i in (list(set(list(np.concatenate(grausLib))))):

		if i not in NoX:
			lista_temporaria.append(1)
		else:
			lista_temporaria.append(0)

		if len(lista_temporaria) == 2:
			lista.append(lista_temporaria)
			lista_temporaria = []

	return old_global, Global, lista

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

def makePointList(coordinates, incidences):

    point_list = []
    
    for i in range(len(incidences)):

        indexA = int(incidences[i][1]) 
        indexB = int(incidences[i][2])

        incidence_list = []

        pointA = [coordinates[indexA][1], coordinates[indexA][2]]
        incidence_list.append(pointA)
        pointB = [coordinates[indexB][1], coordinates[indexB][2]]
        incidence_list.append(pointB)

        point_list.append(incidence_list)

    return point_list

def makeLib(incidences):

    lib = []

    j = 0

    for i in range(len(incidences)):

        indexA = int(incidences[i][1]) 
        indexB = int(incidences[i][2])

        incidence_list = []

    return lib
    


def makeRigidMatrixList(point_list, incidences, materials, geometric): ## [[[1,1][2,2]][[3,3][4,4]]]

    listM = []
    
    for i in range(len(incidences)):

        pointA = point_list[i][0]
        pointB = point_list[i][1]

        e = materials[i+1][0]
        a = geometric[i+1][0]
        l = m.hypot(pointB[0] - pointA[0], pointB[1] - pointA[1])
        
        listM.append(calcMRigidez(e, a, l, pointA, pointB))

    return listM

def calcStrainsNStresses(point_list, incidences, materials, u):
    
    strains = []
    stresses = []

    for i in range(len(incidences)):

        up = []

        pointA = point_list[i][0]
        pointB = point_list[i][1]

        e = materials[i+1][0]
        l = m.hypot(pointB[0] - pointA[0], pointB[1] - pointA[1])
        
        indexA = int(incidences[i][1]) - 1
        indexB = int(incidences[i][2]) - 1

        up.append(u[indexA][0])
        up.append(u[indexA][1])
        up.append(u[indexB][0])
        up.append(u[indexB][1])

        x = calcProdutoEscalar(pointA, pointB, up) ####

        strains.append(x/l)
        stresses.append(x*e/l)

    return strains, stresses

def makeLoads(loads, u_template):

    F = []

    return F

def makeReactionForces():

    rForces = []

    return rForces


def finalU(ut, u_template):
    
    u = []
     #preenche a matriz u corretamente no formato u = [[1, 2], [3, 4]]
    return u

def makeExitFile(filename, u, strains, stresses, forces):
    
    file = open(filename,"w")
    file.write("*DISPLACEMENTS\n")
    j = 1
    for i in range(len(u)):
        file.write(str(j) + " " + str(u[i][0]) + " " + str(u[i][1]) + "\n")
        j += 1
    file.write("\n"+"*ELEMENT_STRAINS\n")
    j = 1
    for i in range(len(strains)):
        file.write(str(j) + " " + str(strains[i]) + "\n")
        j += 1
    file.write("\n"+"*ELEMENT_STRESSES\n")
    j = 1
    for i in range(len(stresses)):
        file.write(str(j) + " " + str(stresses[i]) + "\n")
        j += 1
    file.write("\n"+"*REACTION_FORCES\n")

def main():

    #M = np.array([[1.59e8,-0.40e8,-0.54e8],
    #            [-0.40e8,1.70e8,0.40e8],
    #            [-0.54e8,0.40e8,0.54e8],])

    #F=np.array([[0.0],[150.0],[-100]])

    #u = calcGauss(F, M, 0.005, 10)+[10]
    
    dic = readDic("data.txt")
    coordinates = dic["*COORDINATES"]
    incidences = dic["*INCIDENCES"]
    geometric = dic["*GEOMETRIC_PROPERTIES"]
    materials = dic["*MATERIALS"]
    restrictions = dic["*BCNODES"][1:]
    loads = dic["*LOADS"][1:]

    point_list = makePointList(coordinates, incidences)

    listM = makeRigidMatrixList(point_list, incidences, materials, geometric)

    lib = makeLib(incidences) #!

    calcGlobal = retornaglobalpronta(listM, lib, restrictions)
    globalM = calcGlobal[0]
    globalMrestricted = calcGlobal[1]
    u_template = calcGlobal[2]

    F = makeLoads(loads, u_template) #!

    tolerancia = 0.005
    loopN = 10

    ut = calcGauss(F, globalMrestricted, tolerancia, loopN)
    
    u = finalU(ut, u_template) #! 

    calcsns = calcStrainsNStresses(point_list, incidences, materials, u)
    strains = calcsns[0]
    stresses = calcsns[1]
    rForces = makeReactionForces(u, globalM) #!

    makeExitFile("saida.txt", u, strains, stresses, rForces) #!

main()
