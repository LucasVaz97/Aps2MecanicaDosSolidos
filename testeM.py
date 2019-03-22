import numpy as np
import math as m

pontoA=[0,0]
pontoB=[0,0.4]
l=0.4
a=2e-4
e=210e9
alfa= m.atan2(pontoB[1]-pontoA[1],pontoB[0]-pontoA[0])
c=m.cos(alfa)
s=m.sin(alfa)


M = np.array([[c**2,c*s,-c**2,-c*s],
[c*s,s**2,-c*s,-s**2],
[-c**2,-c*s,c**2,c*s],
[-c*s,-s**2,c*s,s**2]])


M=M.round(7)
print((e*a/l)*M)
