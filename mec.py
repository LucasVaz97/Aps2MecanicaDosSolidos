from anastruct import SystemElements
import numpy as np
import math as m


def calcScalar(p1, p2, vector):

    x = (p2[0] - p1[0])
    y = (p2[1] - p1[1])
    h = (x**2 + y**2)**(1/2)

    CS = [0, 0, 0, 0]
    CS[0] = - (x/h)
    CS[1] = - (y/h)
    CS[2] = (x/h)
    CS[3] = (y/h)

    return np.dot(CS, vector)


def createGlobal(matrices, lib, restriction):

    lib = np.array(lib).astype(int)

    No = []

    for i in range(len(restriction)):
        No.append(restriction[i][0]*2 - 2 + restriction[i][1])

    size = len(set(list(np.concatenate(lib))))

    Global = np.zeros((size, size), dtype='float')

    for i in range(len(matrices)):
        for x in range(len(matrices[i])):
            for y in range(len(matrices[i])):
                Global[lib[i][y] - 1, lib[i][x] - 1] += matrices[i][y, x]

    _list = []
    t_list = []

    No = np.array(No)
    No -= 1

    old_global = Global
    Global = np.delete(Global, No, 0)
    Global = np.delete(Global, No, 1)

    No += 1

    for i in (list(set(list(np.concatenate(lib))))):

        if i not in No:
            t_list.append(1)
        else:
            t_list.append(0)

        if len(t_list) == 2:
            _list.append(t_list)
            t_list = []

    return old_global, Global, _list


def readDic(filename):
    dic = {}
    f = open(filename, "r")
    aux = ""
    for x in f:
        if(x[0] == "*"):
            aux = x.rstrip()
            dic[aux] = []
        if(x[0] != '*'):
            dic[aux].append(x.rstrip())
    for i in dic:
        for j in range(len(dic[i])):
            dic[i][j] = dic[i][j].split()
            for k in range(len(dic[i][j])):
                try:
                    dic[i][j][k] = float(dic[i][j][k])
                except ValueError:
                    p = 0
    return dic


def calcMRigid(e, a, l, pointA, pointB):
    alpha = m.atan2(pointB[1]-pointA[1], pointB[0]-pointA[0])
    c = m.cos(alpha)
    s = m.sin(alpha)
    M = np.array([[c**2, c*s, -c**2, -c*s],
                  [c*s, s**2, -c*s, -s**2],
                  [-c**2, -c*s, c**2, c*s],
                  [-c*s, -s**2, c*s, s**2]])
    M = M.round(7)
    return ((e*a/l)*M)


def calcGauss(F, M, tolerance, loopN):

    u = [0]*len(M[0])
    uv = [0]*len(M[0])

    checkt2 = 0
    loop = 0

    while(True and (loop < loopN)):

        index = 0
        checkt1 = 0

        for i in range(len(M)):
            _sum = 0

            for j in range(len(M[i])):
                _sum += M[i][j]*u[j]

            uv[i] = u[i]
            u[i] = (F[i] - _sum + u[i] * M[i][index]) / M[i][index]
            index += 1

            if(loop > 0):
                if u[i] != 0:
                    check = (u[i] - uv[i]) / u[i]

                    if(check > checkt1):
                        checkt1 = check

        if(loop > 0):
            checkt2 = checkt1

            if(checkt2 < tolerance):
                break

        loop += 1

    return u


def calcJacobi(F, M, tolerance, loopN):

    u = [0]*len(M[0])
    uv = [0]*len(M[0])

    checkt2 = 0
    loop = 0

    while(True and (loop < loopN)):

        index = 0
        checkt1 = 0

        for i in range(len(M)):
            _sum = 0

            uv[i] = u[i]

            for j in range(len(M[i])):
                _sum += M[i][j]*uv[j]

            u[i] = (F[i] - _sum + uv[i] * M[i][index]) / M[i][index]
            index += 1

            if(loop > 0):
                if u[i] != 0:
                    check = (u[i] - uv[i]) / u[i]

                    if(check > checkt1):
                        checkt1 = check

        if(loop > 0):
            checkt2 = checkt1

            if(checkt2 < tolerance):
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
        #print(point_list)

    return point_list


def makeLib(incidences):

    lib = []
    for i in range(len(incidences)):
        nisbe = []
        for j in range(len(incidences[i])):
            if(j > 0):
                for k in range(2):
                    if(k == 0):
                        nisbe.append((incidences[i][j]*2)-1)
                    else:
                        nisbe.append((incidences[i][j]*2))

        lib.append(nisbe)

    return lib


def makeRigidMatrixList(point_list, incidences, materials, geometric):

    listM = []

    for i in range(len(incidences)):

        pointA = point_list[i][0]
        pointB = point_list[i][1]

        e = materials[i+1][0]
        a = geometric[i+1][0]
        l = m.hypot(pointB[0] - pointA[0], pointB[1] - pointA[1])

        listM.append(calcMRigid(e, a, l, pointA, pointB))

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

        x = calcScalar(pointA, pointB, up)

        strains.append(x/l)
        stresses.append(x*e/l)

    return strains, stresses


def makeLoads(loads, u_template):

    F = []

    for i in range(len(u_template)):
        hasAppended1 = False
        hasAppended2 = False

        for j in range(len(loads)):
            if(u_template[i][0] == 1):

                if((loads[j][0] == i+1) and (loads[j][1] == 1)):

                    if(not hasAppended1):
                        F.append(loads[j][2])
                        hasAppended1 = True

            if(u_template[i][1] == 1):

                if((loads[j][0] == i+1) and (loads[j][1] == 2)):

                    if(not hasAppended2):
                        F.append(loads[j][2])
                        hasAppended2 = True

        if(not hasAppended1 and u_template[i][0] == 1):
            F.append(0)

        if(not hasAppended2 and u_template[i][1] == 1):
            F.append(0)

    return F


def makeReactionForces(vetor, matriz):
    v = np.concatenate(np.array(vetor))
    m = np.array(matriz)
    retorna = m.dot(v)
    listinha = []
    retmesmo = []
    for i in range(len(retorna)):
        listinha.append(retorna[i])
        if len(listinha) == 2:
            retmesmo.append(listinha)
            listinha = []
    return retmesmo


def finalU(lista_de_valores, lista_de_zeros_e_uns):
    listaReturn = []

    for i in range(len(lista_de_zeros_e_uns)):
        apenda = []
        for j in range(len(lista_de_zeros_e_uns[i])):
            if lista_de_zeros_e_uns[i][j] == 0:
                apenda.append(0)
            else:
                apenda.append(lista_de_valores[0])
                del lista_de_valores[0]

        listaReturn.append(apenda)

    return listaReturn


def makeExitFile(filename, u, strains, stresses, rForces, u_template):

    file = open(filename, "w")
    file.write("*DISPLACEMENTS\n")
    for i in range(len(u)):
        file.write(str(i + 1) + " ")
        for j in range(len(u[i])):
            file.write(str(u[i][j]))
            if j == len(u[i]) - 1:
                file.write("\n")
            else:
                file.write(" ")

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
    for i in range(len(rForces)):
        for j in range(len(rForces[i])):
            if u_template[i][j] == 0:
                file.write(str(i + 1) + " ")
                if j == 0:
                    file.write("FX = ")
                elif j == 1:
                    file.write("FY = ")
                file.write(str(rForces[i][j]))
                file.write("\n")


def plotGraphGroup(point_list, displaced_point_list):
    ss = SystemElements(EA=15000, EI=5000)

    for i in range(len(point_list)):
        ss.add_element(location=[point_list[i][0], point_list[i][1]])

    for i in range(len(displaced_point_list)):
        ss.add_element(location=[displaced_point_list[i]
                                 [0], displaced_point_list[i][1]])

    ss.show_structure()


def plotGraph(point_list):
    ss = SystemElements(EA=15000, EI=5000)

    for i in range(len(point_list)):
        ss.add_element(location=[point_list[i][0], point_list[i][1]])

    ss.show_structure()



def makeDisplacedCoordinates(coordinates, u):

    num = coordinates[0]
    coordinates = np.array(coordinates[1:])[:, 1:] + u
    lista = [num]

    for i in range(len(coordinates)):
        listinha = [i + 1]
        for j in range(len(coordinates[i])):
            listinha.append(coordinates[i][j])
        lista.append(listinha)

    return lista


def main():
    name = input("Nome do arquivo: ")
    dic = readDic(name)
    coordinates = dic["*COORDINATES"]
    incidences = dic["*INCIDENCES"]
    geometric = dic["*GEOMETRIC_PROPERTIES"]
    materials = dic["*MATERIALS"]
    restrictions = dic["*BCNODES"][1:]
    loads = dic["*LOADS"][1:]

    point_list = makePointList(coordinates, incidences)

    plotGraph(point_list)

    listM = makeRigidMatrixList(point_list, incidences, materials, geometric)

    lib = makeLib(incidences)

    calcGlobal = createGlobal(listM, lib, restrictions)
    globalM = calcGlobal[0]
    globalMrestricted = calcGlobal[1]
    u_template = calcGlobal[2]

    F = makeLoads(loads, u_template)

    selection = int(input("Selecione o método: Gauss(1) ou Jacobi(2): "))
    tolerance = float(input("Tolerancia: "))
    loopN = int(input("Numero de iterações: "))
    if(selection == 1):
        ut = calcGauss(F, globalMrestricted, tolerance, loopN)
    elif(selection == 2):
        ut = calcJacobi(F, globalMrestricted, tolerance, loopN)

    u = finalU(ut, u_template)

    calcsns = calcStrainsNStresses(point_list, incidences, materials, u)
    strains = calcsns[0]
    stresses = calcsns[1]
    rForces = makeReactionForces(u, globalM)

    displaced_coordinates = makeDisplacedCoordinates(coordinates, u)
    displaced_point_list = makePointList(displaced_coordinates, incidences)

    plotGraph(displaced_point_list)
    plotGraphGroup(point_list, displaced_point_list)

    makeExitFile("saida.fem", u, strains, stresses, rForces, u_template)


main()
