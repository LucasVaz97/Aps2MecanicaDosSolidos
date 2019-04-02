import math as m
import numpy as np

def calcMRigid(e, a, l, pointA, pointB):
    alpha = m.atan2(pointB[1]-pointA[1], pointB[0]-pointA[0])
    c = m.cos(alpha)
    s = m.sin(alpha)
    M = np.array([[c**2, c*s, -c**2, -c*s],
                  [c*s, s**2, -c*s, -s**2],
                  [-c**2, -c*s, c**2, c*s],
                  [-c*s, -s**2, c*s, s**2]])
    #M = M.round(7)
    print((e*a/l)*M)



calcMRigid(210e9,2e-4,0.5,[0,0],[0.3,0.4])

#this is an ammend test
