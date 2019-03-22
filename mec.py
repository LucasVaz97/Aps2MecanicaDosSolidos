import numpy as np

dic={}
f = open("data.txt", "r")
auxiliar=""
for x in f:
    if(x[0]=="*"):
        auxiliar=x.rstrip()
        dic[auxiliar]=[]
        counter=0
    if(x[0]!='*'):
        dic[auxiliar].append(x.rstrip())

for i in dic:
    for j in range(len(dic[i])):
        dic[i][j]=dic[i][j].split()
        for k in range(len(dic[i][j])):
            try:
                dic[i][j][k]=float(dic[i][j][k])
            except ValueError:
                p=0;

def calcMRigidez(E,A,l,ponto1,ponto2):



print(dic["*ELEMENT_GROUPS"][1][0])
