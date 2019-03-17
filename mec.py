
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

print(dic["*MATERIALS"][1][0]-1000)
